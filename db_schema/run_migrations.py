from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .db_extensions import database
from flask_migrate import Migrate

from db_schema import *
app = Flask(__name__)

app.config.from_object('db_schema.config.Config')
database.init_app(app)

migrate = Migrate(app, database)