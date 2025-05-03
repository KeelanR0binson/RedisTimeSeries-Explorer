import pytest
from unittest.mock import Mock, patch
import pandas as pd
from datetime import datetime
from redis_utils import get_redis_connection, get_timeseries_keys, get_timeseries_data

@pytest.fixture
def mock_redis():
    with patch('redis.Redis') as mock:
        yield mock

@pytest.fixture
def mock_redis_client():
    client = Mock()
    client.keys.return_value = [b'ts:key1', b'ts:key2']
    client.type.return_value = b'TSDB-TYPE'
    client.ts.return_value.range.return_value = [
        (1609459200000, 1.0),  # 2021-01-01 00:00:00
        (1609545600000, 2.0),  # 2021-01-02 00:00:00
    ]
    return client

def test_get_redis_connection(mock_redis):
    get_redis_connection(host='localhost', port=6379, db=0)
    mock_redis.assert_called_once_with(host='localhost', port=6379, db=0)

def test_get_timeseries_keys(mock_redis_client):
    keys = get_timeseries_keys(mock_redis_client)
    assert keys == ['ts:key1', 'ts:key2']
    mock_redis_client.keys.assert_called_once()
    assert mock_redis_client.type.call_count == 2

def test_get_timeseries_data(mock_redis_client):
    df = get_timeseries_data(mock_redis_client, 'ts:key1', 1609459200000, 1609545600000)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ['timestamp', 'value']
    assert df['timestamp'].iloc[0] == pd.Timestamp('2021-01-01 00:00:00')
    assert df['value'].iloc[0] == 1.0

def test_get_timeseries_data_empty(mock_redis_client):
    mock_redis_client.ts.return_value.range.return_value = []
    df = get_timeseries_data(mock_redis_client, 'ts:key1')
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0
    assert list(df.columns) == ['timestamp', 'value'] 