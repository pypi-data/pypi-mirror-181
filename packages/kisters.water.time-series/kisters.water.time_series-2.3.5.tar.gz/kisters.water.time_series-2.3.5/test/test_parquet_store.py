import pytest

from kisters.water.time_series.test import TimeSeriesStoreAsyncTest, TimeSeriesStoreBasicTest


@pytest.mark.usefixtures("parquet_store_cls")
class TestBasicParquetStore(TimeSeriesStoreBasicTest):
    """"""


@pytest.mark.usefixtures("parquet_store_cls")
class TestAsyncParquetStore(TimeSeriesStoreAsyncTest):
    """"""
