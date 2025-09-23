import pytest
from aggregator import Aggregator


def test_aggregator_update_and_merge():
    agg1 = Aggregator()
    row = {"client_id": "CUST1", "category": "shopping"}
    agg1.update(row, 100)
    assert agg1.clients["CUST1"]["total_rub"] == 100
    assert agg1.clients["CUST1"]["count"] == 1
    assert agg1.categories["shopping"] == 100

    agg2 = Aggregator()
    agg2.update(row, 50)
    agg1.merge(agg2)
    assert agg1.clients["CUST1"]["total_rub"] == 150
    assert agg1.clients["CUST1"]["count"] == 2
    assert agg1.categories["shopping"] == 150
