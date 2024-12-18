from flask import Blueprint
from controllers.data_controller import get_processed_data

data_routes = Blueprint('data_routes', __name__)

@data_routes.route('/data', methods=['GET'])
def get_data():
    return get_processed_data()