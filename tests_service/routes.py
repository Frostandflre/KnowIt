import requests
from flask import Blueprint,request,jsonify
from db_schema.tests_service_models import Tests,TestCards,UserResults
from db_schema.db_extensions import database
from sqlalchemy import func


tests = Blueprint("tests",__name__)

API_GATEWAY_URL = "http://localhost:5005"

@tests.route("/get_test_cards", methods=["GET"])
def get_test_cards():
    profession = request.args.get("profession")
    if not profession:
        return jsonify({"error": "Произошла ошибка,тесты не найдены"}), 404

    raw_test_cards = (
    database.session.query(
        TestCards.id,
        TestCards.profession,
        TestCards.course,
        TestCards.test_title
    )
    .filter_by(profession=profession)
    .order_by(TestCards.course)
    .all()
)
    test_cards = [
    {
        'id': card.id,
        'profession': card.profession,
        'course': card.course,
        'test_title': card.test_title,
    }

    for card in raw_test_cards
]

    if not test_cards:
        return jsonify({"error": "Произошла ошибка,тесты не найдены"}), 404

    return jsonify({"message": "Статус получен","test_cards":test_cards}),200

@tests.route("/get_test", methods=["GET"])
def get_test():
    test_title = request.args.get("test_title")
    if not test_title:
        return jsonify({"error": "Произошла ошибка,тесты не найдены"}), 404

    test = [question.to_dict() for question in Tests.query.filter_by(test_title=test_title).all()]

    if not test:
        return jsonify({"error": "Произошла ошибка,тесты не найдены"}), 404

    return jsonify({"message": "Статус получен","test":test}),200

@tests.route("/get_user_tests_results", methods=["GET"])
def get_user_tests_results():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Произошла ошибка,пользователь не найден"}), 404

    user_results = [result.to_dict() for result in UserResults.query.filter_by(user_id=user_id).all()]

    return jsonify({"message": "Статус получен","user_results":user_results}),200

@tests.route("/save_results", methods=["POST"])
def save_results():
    test_title = request.args.get("test_title")
    if not test_title:
        return jsonify({"error": "Произошла ошибка,тест не найден"}), 404

    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Произошла ошибка,Пользователь не найден"}), 404

    score = request.args.get("score")
    if not score :
        return jsonify({"error": "Произошла ошибка,Результат не найден"}), 404

    new_result = UserResults(user_id=user_id,test_title=test_title,score=score)
    database.session.add(new_result)
    database.session.commit()

    average_score = database.session.query(func.avg(UserResults.score)).filter(
        UserResults.user_id == user_id
    ).scalar()

    average_score = round(average_score, 2)/10 * 100 if average_score else 0

    requests.post(f"{API_GATEWAY_URL}/update_average_score",params={"user_id": user_id, "average_score": average_score})

    return jsonify({"message": "Результаты сохранены"}),200
