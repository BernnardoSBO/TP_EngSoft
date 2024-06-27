import pytest
from datetime import datetime, timedelta, timezone

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from routes.AuthRoutes import token_is_expired


#using datetime.now here doesnt make this test flaky
#any datetime could be used here
@pytest.mark.parametrize(
    "exp_timestamp, delta, time, expected",
    [
        (None, 10, datetime.now(timezone.utc), True),  #test when exp_timestamp is None
        (datetime.timestamp(datetime.now(timezone.utc) + timedelta(minutes=15)), 10, datetime.now(timezone.utc), False), 
        (datetime.timestamp(datetime.now(timezone.utc) + timedelta(minutes=5)), 10, datetime.now(timezone.utc), True),  
        (datetime.timestamp(datetime.now(timezone.utc) + timedelta(minutes=10)), 10, datetime.now(timezone.utc), True),  
        (datetime.timestamp(datetime.now(timezone.utc) + timedelta(minutes=10)), -10, datetime.now(timezone.utc), False)  
    ]
)
def test_token_is_expired(exp_timestamp, delta, time, expected):
    assert token_is_expired(exp_timestamp, delta, time) == expected
