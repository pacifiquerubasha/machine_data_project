from flask import Flask
from routes.data_routes import data_routes
from routes.status_routes import status_routes

app = Flask(__name__)

# Register routes
app.register_blueprint(data_routes, url_prefix='/api')
app.register_blueprint(status_routes, url_prefix='/api')

@app.route('/', methods=['GET'])
def get_status():
    return {"status": "API is running!"}

if __name__ == '__main__':
    app.run(debug=True, port=5000)