from flask import Flask
from .routes import gateway

def create_gateway_app():
    app = Flask(__name__)

    app.register_blueprint(gateway)

    return app