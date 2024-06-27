import pytest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from routes.ProductsRoutes import create_product_from_request  
from unittest.mock import MagicMock



@pytest.fixture
def mock_request():
    request = MagicMock()
    request.json = {
        "name": "Test Product",
        "description": "This is a test product description.",
        "price": 10.99,
        "stock": 100
    }
    return request

def test_create_product_from_request_valid(mock_request):
    vendor_id = "vendor123"
    product = create_product_from_request(mock_request, vendor_id)
    
    assert product.name == "Test Product"
    assert product.description == "This is a test product description."
    assert product.price == 10.99
    assert product.stock == 100
    assert product.vendor_id == vendor_id

def test_create_product_from_request_exceed_max_lengths(mock_request):
    vendor_id = "vendor123"
    # Modify the request to exceed max lengths
    mock_request.json["name"] = "A" * 60
    mock_request.json["description"] = "B" * 150
    
    product = create_product_from_request(mock_request, vendor_id)
    
    # Check that the name and description are truncated to max lengths
    assert len(product.name) == 50
    assert len(product.description) == 100

def test_create_product_from_request_missing_fields():
    request = MagicMock()
    request.json = {
        "name": "Test Product",
        "description": "This is a test product description.",
        # Missing "price" and "stock"
    }
    vendor_id = "vendor123"
    
    product = create_product_from_request(request, vendor_id)
    
    # Check that the product object is created with default values for missing fields
    assert product.name == "Test Product"
    assert product.description == "This is a test product description."
    assert product.price is None  
    assert product.stock is None  
    assert product.vendor_id == vendor_id
