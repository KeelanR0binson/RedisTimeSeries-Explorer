# Redis TimeSeries Explorer

A Streamlit application for visualizing Redis TimeSeries data. This tool provides an intuitive interface for exploring and analyzing time series data stored in Redis with the RedisTimeSeries module.

## Features

- Connect to any Redis instance with RedisTimeSeries module
- Browse available TimeSeries keys
- Visualize TimeSeries data with interactive plots
- Filter data by date range
- View raw data in a table format
- Error handling and input validation
- Responsive and user-friendly interface

## Installation

### Prerequisites

- Python 3.7 or higher
- Redis server with RedisTimeSeries module installed
- pip (Python package installer)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/KeelanR0binson/RedisTimeSeries-Explorer.git
cd RedisTimeSeries-Explorer
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Redis server with RedisTimeSeries module
2. Run the Streamlit app:
```bash
streamlit run app.py
```

3. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

### Using the Application

1. **Connect to Redis**:
   - Enter the Redis host (default: localhost)
   - Enter the Redis port (default: 6379)
   - Select the Redis database (default: 0)
   - Click "Connect"

2. **Select TimeSeries Key**:
   - Choose a TimeSeries key from the dropdown menu
   - Available keys are automatically detected

3. **Set Date Range**:
   - Select start and end dates
   - Select start and end times
   - The application will validate that the end time is after the start time

4. **View Data**:
   - Interactive plot showing the time series data
   - Raw data table below the plot
   - Hover over data points for detailed information


## Acknowledgments

- [Redis](https://redis.io/) - The in-memory data structure store
- [RedisTimeSeries](https://oss.redis.com/redistimeseries/) - Redis module for time series data
- [Streamlit](https://streamlit.io/) - The web framework used
- [Plotly](https://plotly.com/) - The visualization library used
