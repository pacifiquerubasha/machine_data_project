import os
import json
from typing import List, Tuple, Dict


def calculate_average(values: List[float]) -> float:
    """
    Calculate the average of a list of values.
    
    Args:
        values (List[float]): List of values
    
    Returns:
        float: Average of the values
    """
    return round(sum(values) / len(values), 2) if values else 0

def detect_anomalies(values: List[float], threshold: float = 0.2) -> List[Dict]:
    """
    Detect anomalies in the dataset.
    
    Args:
        values (List[float]): Machine values
        threshold (float): Percentage deviation to consider an anomaly
    
    Returns:
        List[Dict]: List of detected anomalies
    """
    if len(values) < 2:
        return []
    
    
    average = sum(values) / len(values)
    
    anomalies = []
    
    for i, value in enumerate(values):
        deviation = abs(value - average) / average
        
        if deviation > threshold:
            anomalies.append({
                'index': i,
                'value': value,
                'deviation_percentage': round(deviation * 100, 2)
            })
    
    return anomalies

def analyze_data(filename: str = 'machine_data.json') -> Dict:
    """
    Perform comprehensive data analysis on machine values.
    
    Args:
        filename (str): Path to the JSON file containing machine data
    
    Returns:
        Dict: Comprehensive analysis results
    """

    # Path to the 'data' folder at the same level as our 'current' folder
    base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_folder = os.path.join(base_directory, 'data')
    filepath = os.path.join(data_folder, filename)

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error reading data from {filename}")
        return {}
    
    if not data:
        raise ValueError("Empty dataset provided")
    
    # Temperature and speed values
    temperature_values = [entry['temperature'] for entry in data]
    speed_values = [entry['speed'] for entry in data]
    
    # Determine period (start and end)
    period_start = data[0]['timestamp'] if data else None
    period_end = data[-1]['timestamp'] if data else None
    
    analysis = {
        'temperature': {
            'average': calculate_average(temperature_values),
            'min': min(temperature_values),
            'max': max(temperature_values),
            'total_readings': len(temperature_values),
            'anomalies': detect_anomalies(temperature_values)
        },
        'speed': {
            'average': calculate_average(speed_values),
            'min': min(speed_values),
            'max': max(speed_values),
            'total_readings': len(speed_values),
            'anomalies': detect_anomalies(speed_values)
        },
        'period': {
            'start': period_start,
            'end': period_end
        }
    }
    
    return analysis

if __name__ == "__main__":
    try:
        results = analyze_data()
        print(results)
    except ValueError as e:
        print(f"Error: {e}")