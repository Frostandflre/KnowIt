import requests
from flask import Blueprint,render_template

main = Blueprint("main",__name__)

API_GATEWAY_URL = "http://localhost:5005"

@main.route("/")
def main_page():
    return render_template("main_page.html")