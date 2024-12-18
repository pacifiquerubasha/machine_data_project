from flask import jsonify, request
from datetime import datetime

ALLOWED_STATUSES = ['IDLE', 'STARTED', 'IN_PROGRESS', 'PAUSED', 'COMPLETED']

# In-memory status tracking
machine_status = {
    'current_status': 'IDLE',
    'last_updated': None
}

def update_status():
    """
    Endpoint to update machine status.
    
    Validates and updates machine status.
    
    Returns:
        JSON: Status update confirmation or error message
    """
    data = request.get_json()
    
    # Input validation
    if not data or 'status' not in data:
        return jsonify({"error": "Status is required"}), 400
    
    new_status = data['status'].upper()
    
    if new_status not in ALLOWED_STATUSES:
        return jsonify({
            "error": f"Invalid status. Allowed statuses: {', '.join(ALLOWED_STATUSES)}"
        }), 400
    
    # Update status
    machine_status['current_status'] = new_status
    machine_status['last_updated'] = str(datetime.now())
    
    return jsonify({
        "message": "Status updated successfully",
        "current_status": machine_status
    }), 200