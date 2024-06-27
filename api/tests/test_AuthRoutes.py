import pytest
from datetime import datetime, timedelta, timezone

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
# Mock datetime with a fixed value for testing
from routes.AuthRoutes import token_is_expired

@pytest.fixture
def base_time():
    return datetime(2024, 6, 25, 12, 0, 0, tzinfo=timezone.utc)

def test_token_is_expired_when_exp_timestamp_is_none():
    exp_timestamp = None
    delta = 10  
    assert token_is_expired(exp_timestamp, delta) is True

def test_token_when_not_expired(base_time):
  
    exp_timestamp = datetime.timestamp(base_time + timedelta(minutes=15))  
    delta = 10  
    
    assert token_is_expired(exp_timestamp, delta, time=base_time) is False

def test_token_when_expired(base_time):
   
    exp_timestamp = datetime.timestamp(base_time + timedelta(minutes=5)) 
    delta = 10 
    
    assert token_is_expired(exp_timestamp, delta, time=base_time) is False

