import json
import random
import time
from datetime import datetime
import threading
import os

def generate_machine_data():
    """
    Generate simulated machine data with random variations.
    
    Returns:
        dict: A dictionary containing machine data with timestamp
    """
    return {
        'timestamp': datetime.now().isoformat(),
        'temperature': round(random.uniform(20.0, 30.0), 2),
        'speed': round(random.uniform(40.0, 60.0), 2),
        'status': random.choice(['IDLE', 'RUNNING', 'PAUSED'])
    }

def save_data_to_json(filename='machine_data.json', max_entries=10):
    """
    Save generated machine data to a JSON file.
    
    Args:
        filename (str): Name of the file to save data
        max_entries (int): Maximum number of entries to keep
    """

    # Path to the 'data' folder 
    base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_folder = os.path.join(base_directory, 'data')

    # Check if the 'data' folder exists, if not, create it
    os.makedirs(data_folder, exist_ok=True)

    # Full path to the JSON file
    filepath = os.path.join(data_folder, filename)

    try:
        with open(filepath, 'r') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []
    
    # Generate and append new data
    new_data = generate_machine_data()
    existing_data.append(new_data)
    
    # Keep only last max_entries for simplicity and performance reasons
    existing_data = existing_data[-max_entries:]
    
    with open(filepath, 'w') as f:
        json.dump(existing_data, f, indent=2)
    
    return new_data

def continuous_data_generation(interval=5, filename='machine_data.json'):
    """
    Continuously generate and save machine data at specified intervals.
    
    Args:
        interval (int): Interval between data generations in seconds
        filename (str): JSON file to save data
    """
    def generate_job():
        save_data_to_json(filename)
        # Schedule next run
        threading.Timer(interval, generate_job).start()
    
    # Start the first job
    generate_job()

# Main execution
if __name__ == "__main__":
    print("Starting continuous machine data generation...")
    continuous_data_generation()