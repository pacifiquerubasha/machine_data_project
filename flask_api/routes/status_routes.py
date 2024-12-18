from flask import Blueprint
from controllers.status_controller import update_status

status_routes = Blueprint('status_routes', __name__)

@status_routes.route('/status', methods=['POST'])
def set_status():
    return update_status()