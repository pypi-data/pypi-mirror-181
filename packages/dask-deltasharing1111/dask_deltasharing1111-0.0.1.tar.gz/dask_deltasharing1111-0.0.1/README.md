# Dask Delta Sharing

This library lets you access tables in [Delta Sharing](https://github.com/delta-io/delta-sharing/)
as [Dask DataFrames](https://docs.dask.org/en/stable/dataframe.html).

Usage:

```python
import dask_deltasharing as dds
df = dds.load_as_dask("test-profile.json#main.default.test_table")
```
