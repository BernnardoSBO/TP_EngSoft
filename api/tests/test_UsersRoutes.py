import pytest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from routes.UsersRoutes import *  



@pytest.mark.parametrize(
    "data, expected_page, expected_per_page",
    [
        (None, 1, 3),  
        ({"page": 2, "per_page": 5}, 2, 5),  
        ({"page": 4}, 4, 3),  
        ({"per_page": 10}, 1, 10), 
        ({}, 1, 3) ,
        ({"page": -1, "per_page": 0}, -1, 0)  
    ]
)
def test_get_pagination_params(data, expected_page, expected_per_page):
    page, per_page = get_pagination_params(data)
    assert page == expected_page
    assert per_page == expected_per_page