import pytest
from unittest.mock import Mock
from shop import delivery_cost, place_order


@pytest.mark.parametrize("amount, zone, expected", [
    (0, "city", 1000),
    (9999, "city", 1000),
    (10000, "city", 0),
    (10001, "city", 0),
    (0, "region", 2000),
    (9999, "region", 2000),
    (10000, "region", 0),
    (10001, "region", 0),
])
def test_delivery(amount, zone, expected):
    assert delivery_cost(amount, zone) == expected


@pytest.mark.parametrize("amount, zone, error", [
    (-1, "city", ValueError),
    (12.5, "city", TypeError),
    (True, "city", TypeError),
    (5000, "other", ValueError),
])
def test_invalid_input(amount, zone, error):
    with pytest.raises(error):
        delivery_cost(amount, zone)


@pytest.fixture
def order_data():
    return {"amount": 5000, "zone": "city"}


EXPECTED = {"amount": 5000, "zone": "city", "delivery": 1000, "total": 6000}


def test_order_result(order_data):
    save = Mock()
    result = place_order(order_data["amount"], order_data["zone"], save)
    assert result == EXPECTED


def test_order_saved_once(order_data):
    save = Mock()
    place_order(order_data["amount"], order_data["zone"], save)
    save.assert_called_once_with(EXPECTED)


def test_storage_failure(order_data):
    save = Mock(side_effect=RuntimeError("storage unavailable"))
    with pytest.raises(RuntimeError, match="storage unavailable"):
        place_order(order_data["amount"], order_data["zone"], save)
    save.assert_called_once_with(EXPECTED)
