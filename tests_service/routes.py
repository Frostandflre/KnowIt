from flask import Blueprint,request,jsonify
from .models import Tests,TestCards

tests = Blueprint("tests",__name__)

API_GATEWAY_URL = "http://localhost:5005"

@tests.route("/get_test_cards", methods=["GET"])
def get_test_cards():
    profession = request.args.get("profession")
    if not profession:
        return jsonify({"error": "Произошла ошибка,тесты не найдены"}), 404

    test_cards = {
        "first_course":[test_card.to_dict() for test_card in TestCards.query.filter_by(profession=profession,course=1).all()],
        "second_course": [test_card.to_dict() for test_card in TestCards.query.filter_by(profession=profession, course=2).all()],
        "third_course": [test_card.to_dict() for test_card in TestCards.query.filter_by(profession=profession, course=3).all()],
        "fourth_course": [test_card.to_dict() for test_card in TestCards.query.filter_by(profession=profession, course=4).all()]
    }

    if not test_cards:
        return jsonify({"error": "Произошла ошибка,тесты не найдены"}), 404

    return jsonify({"message": "Статус получен","test_cards":test_cards}),200

@tests.route("/get_test", methods=["GET"])
def get_test():
    test_title = request.args.get("test_title")
    if not test_title:
        return jsonify({"error": "Произошла ошибка,тесты не найдены"}), 404

    test = [question.to_dict() for question in Tests.query.filter_by(test_title=test_title).all()],


    if not test:
        return jsonify({"error": "Произошла ошибка,тесты не найдены"}), 404

    return jsonify({"message": "Статус получен","test":test}),200
