"""
Streamlit application for Redis TimeSeries Explorer.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from redis_utils import (
    get_redis_connection,
    get_timeseries_keys,
    get_timeseries_data,
    RedisConnectionError,
    RedisTimeSeriesError
)

def main():
    """Main application function."""
    st.set_page_config(
        page_title="Redis TimeSeries Explorer",
        layout="wide"
    )
    st.title("Redis TimeSeries Explorer")

    # Redis Connection Form
    st.sidebar.title("Redis Connection")
    host = st.sidebar.text_input("Host", value="localhost")
    port = st.sidebar.number_input("Port", value=6379, min_value=1, max_value=65535)
    db = st.sidebar.number_input("Database", value=0, min_value=0, max_value=15)

    try:
        # Connect to Redis
        redis_client = get_redis_connection(host=host, port=port, db=db)
        
        # Get available timeseries keys
        keys = get_timeseries_keys(redis_client)
        if not keys:
            st.warning("No TimeSeries keys found in the selected Redis database.")
            return
        
        # Key selection
        selected_key = st.selectbox("Select TimeSeries Key", keys)
        
        # Date and time range selection
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=7))
            start_time = st.time_input("Start Time", value=datetime.min.time())
        with col2:
            end_date = st.date_input("End Date", value=datetime.now())
            end_time = st.time_input("End Time", value=datetime.max.time())
        
        # Combine date and time
        start_datetime = datetime.combine(start_date, start_time)
        end_datetime = datetime.combine(end_date, end_time)
        
        if start_datetime >= end_datetime:
            st.error("End date/time must be after start date/time")
            return
        
        # Convert to timestamps
        start_timestamp = int(start_datetime.timestamp() * 1000)
        end_timestamp = int(end_datetime.timestamp() * 1000)
        
        # Get and display data
        df = get_timeseries_data(redis_client, selected_key, start_timestamp, end_timestamp)
        
        if df.empty:
            st.warning("No data found for the selected time range.")
            return
        
        # Create the plot
        fig = px.line(df, x='timestamp', y='value', 
                     title=f'TimeSeries Data for {selected_key}',
                     labels={'value': 'Value', 'timestamp': 'Time'})
        
        # Update layout
        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Value",
            hovermode='x unified'
        )
        
        # Display the plot
        st.plotly_chart(fig, use_container_width=True)
        
        # Display raw data
        st.subheader("Raw Data")
        st.dataframe(df)
        
    except (RedisConnectionError, RedisTimeSeriesError) as e:
        st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 