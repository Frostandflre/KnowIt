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

@gateway.route("/get_user_info", methods=["GET"])
def get_user_info():
    user_id = request.args.get("user_id")

    response = requests.get(f"{AUTH_SERVICE_URL}/get_user_info", params={"user_id": user_id})
    return jsonify(response.json()), response.status_code

@gateway.route("/get_user_tests_results", methods=["GET"])
def get_user_tests_results():
    user_id = request.args.get("user_id")

    response = requests.get(f"{TESTS_SERVICE_URL}/get_user_tests_results", params={"user_id": user_id})
    return jsonify(response.json()), response.status_code

@gateway.route("/get_group_info", methods=["GET"])
def get_group_info():
    group = request.args.get("group")

    response = requests.get(f"{AUTH_SERVICE_URL}/get_group_info", params={"group": group})
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

@gateway.route("/save_results", methods=["POST"])
def save_results():
    test_title = request.args.get("test_title")
    user_id = request.args.get("user_id")
    score = request.args.get("score")

    response = requests.post(f"{TESTS_SERVICE_URL}/save_results", params={"test_title": test_title,"user_id": user_id, "score": score})
    return jsonify(response.json()), response.status_code

@gateway.route("/update_average_score", methods=["POST"])
def update_average_score():
    user_id = request.args.get("user_id")
    average_score = request.args.get("average_score")

    response = requests.post(f"{AUTH_SERVICE_URL}/update_average_score", params={"user_id": user_id, "average_score": average_score})
    return jsonify(response.json()), response.status_code
