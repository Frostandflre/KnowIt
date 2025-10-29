from flask import Blueprint
import requests

gateway = Blueprint("gateway",__name__)

API_AUTH_SERVICE_URL = "http://localhost:5001"