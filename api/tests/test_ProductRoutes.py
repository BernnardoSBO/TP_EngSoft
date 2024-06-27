import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from routes.ProductsRoutes import create_product_from_request
from unittest.mock import MagicMock
from unittest.mock import Mock


class Products:
    def __init__(self, name, description, price, stock, vendor_id):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.vendor_id = vendor_id


@pytest.fixture
def vendor_id():
    return 123


def test_create_product_valid_data(vendor_id):
    request = Mock()
    request.json = {
        "name": "Test Product",
        "description": "This is a test product.",
        "price": 29.99,
        "stock": 100,
    }

    product = create_product_from_request(request, vendor_id)

    assert product.name == "Test Product"
    assert product.description == "This is a test product."
    assert product.price == 29.99
    assert product.stock == 100
    assert product.vendor_id == vendor_id


def test_create_product_missing_name(vendor_id):
    request = Mock()
    request.json = {
        "description": "This is a test product.",
        "price": 29.99,
        "stock": 100,
    }

    with pytest.raises(ValueError, match="Product name is required."):
        create_product_from_request(request, vendor_id)


def test_create_product_invalid_price(vendor_id):
    request = Mock()
    request.json = {
        "name": "Test Product",
        "description": "This is a test product.",
        "price": "invalid_price",
        "stock": 100,
    }

    with pytest.raises(ValueError, match="Invalid price value."):
        create_product_from_request(request, vendor_id)


def test_create_product_negative_stock(vendor_id):
    request = Mock()
    request.json = {
        "name": "Test Product",
        "description": "This is a test product.",
        "price": 29.99,
        "stock": -10,
    }

    with pytest.raises(ValueError, match="Invalid stock value."):
        create_product_from_request(request, vendor_id)
