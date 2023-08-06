"""For creating Dask DataFrames from Delta Sharing."""
import json
from typing import Sequence, Optional

import dask
import dask.dataframe
import delta_sharing
import fsspec
import numpy as np
import pandas as pd
import pyarrow.dataset


def _http_to_file(url: str) -> str:
    """Converts an HTTP URL we got from Delta Sharing into a cloud file system path."""
    gcs = re.match("https://storage.googleapis.com/(?P<path>.*)[?]", url)
    s3 = re.match("https://(?P<bucket>.*?).s3.(?P<region>.*?).amazonaws.com(?P<path>.*?)[?]", url)
    azure = re.match("https://(?P<bucket>.*?).blob.core.windows.net(?P<path>.*?)[?]", url)
    if gcs:
        return "gs://" + gcs.group("path")
    if s3:
        return "s3://" + s3.group("bucket") + s3.group("path")
    if azure:
        return "abfs://" + s3.group("bucket") + s3.group("path")
    raise AssertionError("Could not figure out backing storage for: " + str(url))


def _get_client_and_table(url: str):
    profile, share, schema, table = delta_sharing.delta_sharing._parse_url(url)
    client = delta_sharing.SharingClient(profile)
    table = delta_sharing.protocol.Table(name=table, share=share, schema=schema)
    return client, table


def _list_files_in_table(url: str, **kwargs):
    client, table = _get_client_and_table(url)
    return client._rest_client.list_files_in_table(table, **kwargs)


def _list_table_changes(url: str, start: int, end: int, **kwargs):
    opt = delta_sharing.protocol.CdfOptions(starting_version=start, ending_version=end)
    client, table = _get_client_and_table(url)
    return client._rest_client.list_table_changes(table, opt, **kwargs)


def get_latest_table_version(url: str) -> int:
    """Returns the current version of a Delta Sharing table."""
    client, table = _get_client_and_table(url)
    return client._rest_client.query_table_version(table).delta_table_version


def _load_parquet(
    urls: Sequence[str],
    *,
    schema=None,
    filter=None,
    columns=None,
    pyarrow_schema,
    partition_values: Optional[dict] = None,
) -> pd.DataFrame:
    assert len(urls) > 0
    if partition_values is None:
        partition_values = {}
    fs = fsspec.filesystem(urls[0].split(":")[0])
    ds = pyarrow.dataset.dataset(
        source=urls,
        schema=schema,
        filesystem=fs,
        format="parquet",
    )
    df = ds.to_table(
        filter=filter,
        columns=None if columns is None else [c for c in columns if c not in partition_values],
    ).to_pandas()
    # The partition-level values are not stored in the files but come from the metadata.
    # We add these as columns. The metadata stores the values as strings, so we convert
    # them according to the schema.
    for k, v in partition_values.items():
        if columns is None or k in columns:
            df[k] = pd.Series(v, index=df.index, dtype=pyarrow_schema[k])
    return df


def _delta_schema_to_pyarrow_schema(fields: Sequence[dict]) -> dict:
    replace_types = {"string": "str", "integer": "int"}
    meta = {}
    for f in fields:
        t = f["type"].lower()
        meta[f["name"]] = np.dtype(replace_types.get(t, t))
    return meta


def load_as_dask(
    url: str,
    *,
    num_partitions: Optional[int] = None,
    direct_access: bool = False,
    # Passed to PyArrow:
    schema=None,
    filter=None,
    columns=None,
    # Passed to Delta Sharing:
    version: Optional[int] = None,
    predicateHints: Optional[Sequence[str]] = None,
    limitHint: Optional[int] = None,
) -> dask.dataframe.DataFrame:
    """Reads a Delta Sharing table into a Dask DataFrame.

    :param url: The table "URL" in the Delta Sharing format: <profile>#<share>.<schema>.<table>
    :param num_partitions: The number of partitions to create. If None, uses the partitioning from Delta Sharing.
    :param direct_access: Set to True to sidestep HTTP and read the files directly from S3/GCS/Azure.
    """
    res = _list_files_in_table(
        url, version=version, predicateHints=predicateHints, limitHint=limitHint
    )
    fields = json.loads(res.metadata.schema_string)["fields"]
    pyarrow_schema = _delta_schema_to_pyarrow_schema(fields)
    if columns:
        pyarrow_schema = {k: v for (k, v) in pyarrow_schema.items() if k in columns}
    partitioned_by = res.metadata.partition_columns
    if direct_access:
        # Convert the URLs.
        for f in res.add_files:
            f.url = _http_to_file(f.url)
    if num_partitions:
        assert not partitioned_by, "num_partitions is not supported for data-partitioned sources"
        assert (
            len(res.add_files) >= num_partitions
        ), f"{url} only has {len(res.add_files)} partitions, not {num_partitions}"
        # Greedily pack the files into the given number of partitions.
        delta_parts = [{"urls": []} for _ in range(num_partitions)]
        sizes = [0 for _ in range(num_partitions)]
        urls = sorted([(f.size, f.url) for f in res.add_files], reverse=True)
        for size, url in urls:
            i = np.argmin(sizes)
            sizes[i] += size
            delta_parts[i]["urls"].append(url)
    else:
        delta_parts = [
            {"urls": [f.url], "partition_values": f.partition_values} for f in res.add_files
        ]
    # Create DataFrame.
    partitions = []
    for p in delta_parts:
        partitions.append(
            dask.delayed(_load_parquet, name="reading Delta Sharing: " + ",".join(p["urls"]))(
                p["urls"],
                pyarrow_schema=pyarrow_schema,
                schema=schema,
                filter=filter,
                columns=columns,
                partition_values=p.get("partition_values"),
            )
        )
    return dask.dataframe.from_delayed(partitions, meta=pyarrow_schema)
