import json
import time
import threading
from typing import List, Dict
import os

def calculate_moving_average(window: List[float], decimals: int = 2) -> float:
    """
    Calculate moving average for a given window of values.
    
    Args:
        window (List[float]): List of recent values
        decimals (int): Number of decimal places to round
    
    Returns:
        float: Moving average rounded to specified decimals
    """
    return round(sum(window) / len(window), decimals) if window else 0

def process_machine_data(filename: str = 'machine_data.json', window_size: int = 5) -> Dict:
    """
    Read and process machine data, calculating moving averages.
    
    Args:
        filename (str): JSON file containing machine data
        window_size (int): Number of recent readings for moving average
    
    Returns:
        dict: Processed data with moving averages
    """

    base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_folder = os.path.join(base_directory, 'data')
    filepath = os.path.join(data_folder, filename)

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error: Could not read the data file. Might be in the process of creation.")
        return {}
    
    # Ensure we have enough data. Our window size should be less than the total data entries
    if len(data) < window_size:
        print(f"Not enough data. Need at least {window_size} entries.")
        return {}
    
    # Extract recent data for moving averages
    recent_temperatures = [entry['temperature'] for entry in data[-window_size:]]
    recent_speeds = [entry['speed'] for entry in data[-window_size:]]
    
    processed_data = {
        'timestamp': data[-1]['timestamp'],
        'temperature': {
            'latest': data[-1]['temperature'],
            'moving_average': calculate_moving_average(recent_temperatures)
        },
        'speed': {
            'latest': data[-1]['speed'],
            'moving_average': calculate_moving_average(recent_speeds)
        },
        'status': data[-1]['status']
    }


    return processed_data

def continuous_data_processing(interval: int = 10, filename: str = 'machine_data.json'):
    """
    Continuously process machine data at specified intervals.
    
    Args:
        interval (int): Interval between data processing in seconds
        filename (str): JSON file containing machine data
    """
    def process_job():
        processed_data = process_machine_data(filename)
        if processed_data:
            print(json.dumps(processed_data, indent=2))
        
        # Schedule next run
        threading.Timer(interval, process_job).start()
    
    # Start the first job
    process_job()

# Main execution
if __name__ == "__main__":
    print("Starting continuous machine data processing...")
    continuous_data_processing()