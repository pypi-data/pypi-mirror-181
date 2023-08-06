import pytest

from kisters.water.time_series.test import (
    TimeSeriesStoreAsyncTest,
    TimeSeriesStoreBasicTest,
    TimeSeriesStoreCommentsTest,
)


@pytest.mark.usefixtures("memory_store_cls")
class TestBasicMemoryStore(TimeSeriesStoreBasicTest):
    """"""


@pytest.mark.usefixtures("memory_store_cls")
class TestAsyncMemoryStore(TimeSeriesStoreAsyncTest):
    """"""


@pytest.mark.usefixtures("memory_store_cls")
class TestCommentsMemoryStore(TimeSeriesStoreCommentsTest):
    """"""
