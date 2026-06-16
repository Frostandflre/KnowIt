from flask import Flask
from .routes import main
from db_schema.db_extensions import database

def create_main_app():
    app = Flask(__name__)
    app.config.from_object('main_service.config.Config')

    database.init_app(app)

    app.register_blueprint(main)

    return app