from flask import Flask
from .routes import tests
from db_schema.db_extensions import database

def create_tests_app():
    app = Flask(__name__)
    app.config.from_object('tests_service.config.Config')

    database.init_app(app)

    app.register_blueprint(tests)

    return app