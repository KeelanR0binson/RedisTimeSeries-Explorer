"""
Redis utility functions for the Redis TimeSeries Explorer.
"""

import redis
from typing import List, Dict, Any, Optional
import pandas as pd
from datetime import datetime

class RedisConnectionError(Exception):
    """Raised when there is an error connecting to Redis."""
    pass

class RedisTimeSeriesError(Exception):
    """Raised when there is an error with Redis TimeSeries operations."""
    pass

def get_redis_connection(host: str = 'localhost', port: int = 6379, db: int = 0) -> redis.Redis:
    """
    Create and return a Redis connection.
    
    Args:
        host: Redis server hostname
        port: Redis server port
        db: Redis database number
        
    Returns:
        Redis client instance
        
    Raises:
        RedisConnectionError: If connection to Redis fails
    """
    try:
        client = redis.Redis(host=host, port=port, db=db)
        # Test the connection
        client.ping()
        return client
    except redis.ConnectionError as e:
        raise RedisConnectionError(f"Failed to connect to Redis: {str(e)}")

def get_timeseries_keys(redis_client: redis.Redis) -> List[str]:
    """
    Get all timeseries keys from Redis.
    
    Args:
        redis_client: Redis client instance
        
    Returns:
        List of timeseries key names
        
    Raises:
        RedisTimeSeriesError: If there is an error accessing Redis
    """
    try:
        keys = redis_client.keys()
        timeseries_keys = []
        for key in keys:
            if redis_client.type(key) == b'TSDB-TYPE':
                timeseries_keys.append(key.decode('utf-8'))
        return timeseries_keys
    except redis.RedisError as e:
        raise RedisTimeSeriesError(f"Error accessing Redis: {str(e)}")

def get_timeseries_data(
    redis_client: redis.Redis,
    key: str,
    start_time: Optional[int] = None,
    end_time: Optional[int] = None
) -> pd.DataFrame:
    """
    Get timeseries data for a specific key and convert it to a pandas DataFrame.
    
    Args:
        redis_client: Redis client instance
        key: Timeseries key name
        start_time: Start timestamp in milliseconds (optional)
        end_time: End timestamp in milliseconds (optional)
        
    Returns:
        DataFrame containing the timeseries data
        
    Raises:
        RedisTimeSeriesError: If there is an error accessing the timeseries data
    """
    try:
        # Get the raw data
        raw_data = redis_client.ts().range(key, from_time=start_time, to_time=end_time)
        
        # Convert to DataFrame
        if not raw_data:
            return pd.DataFrame(columns=['timestamp', 'value'])
        
        data = [(item[0], item[1]) for item in raw_data]
        df = pd.DataFrame(data, columns=['timestamp', 'value'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        return df
    except redis.RedisError as e:
        raise RedisTimeSeriesError(f"Error accessing timeseries data: {str(e)}") 