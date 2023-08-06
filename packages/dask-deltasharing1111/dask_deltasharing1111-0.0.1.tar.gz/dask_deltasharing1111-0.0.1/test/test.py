"""Temporary test."""
import dask_deltasharing as dds

T = "test-profile.json#lynxkite-dev.default.aml_txns"
print("Plain table:")
print(dds.load_as_dask(T).compute())
print("Plain table with a limit hint: (loads 1 file instead of 4)")
print(dds.load_as_dask(T, limitHint=1).compute())
print("Dask DF partitions normally:")
print(len(list(dds.load_as_dask(T).partitions)))
print("Dask DF partitions with num_partitions=2:")
print(len(list(dds.load_as_dask(T, num_partitions=2).partitions)))

print("Table that has CDF and partitioning:")
T = "test-profile.json#lynxkite-dev.default.aml_txns_partitioned"
print(dds.load_as_dask(T).compute())
print("Latest version:")
print(dds.get_latest_table_version(T))
print("Load version 2 instead:")
print(dds.load_as_dask(T, version=2).compute())
print("Load a specific partition via a predicate hint: (doesn't work)")
print(dds.load_as_dask(T, predicateHints=["century<=20"]).compute())
print("Use PyArrow filtering:")
import pyarrow.compute as pc

print(dds.load_as_dask(T, filter=pc.field("txn_amount") < 200).compute())
print("Get just some columns:")
print(dds.load_as_dask(T, columns=["txn_amount", "beneficiary_id", "century"]).compute())
