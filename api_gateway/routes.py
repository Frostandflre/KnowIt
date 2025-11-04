from flask import Blueprint,request, jsonify
import requests

gateway = Blueprint("gateway",__name__)

AUTH_SERVICE_URL = "http://localhost:5001"
TESTS_SERVICE_URL = "http://localhost:5002"

@gateway.route("/register", methods=["POST"])
def register():
    response = requests.post(f"{AUTH_SERVICE_URL}/register", json=request.json)
    return jsonify(response.json()), response.status_code

@gateway.route("/login", methods=["POST"])
def login():
    response = requests.post(f"{AUTH_SERVICE_URL}/login", json=request.json)
    return jsonify(response.json()), response.status_code

@gateway.route("/get_test_cards", methods=["GET"])
def get_test_cards():
    profession = request.args.get("profession")

    response = requests.get(f"{TESTS_SERVICE_URL}/get_test_cards", params={"profession": profession})
    return jsonify(response.json()), response.status_code

@gateway.route("/get_test", methods=["GET"])
def get_test():
    test_title = request.args.get("test_title")

    response = requests.get(f"{TESTS_SERVICE_URL}/get_test", params={"test_title": test_title})
    return jsonify(response.json()), response.status_code