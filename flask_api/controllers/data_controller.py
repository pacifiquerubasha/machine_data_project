from flask import jsonify
from data_process.data_processor import process_machine_data

def get_processed_data():
    """
    Endpoint to retrieve processed machine data.
    
    Returns:
        JSON: Processed machine data or error message
    """
    try:
        data = process_machine_data()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500