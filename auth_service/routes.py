from flask import Blueprint,request, jsonify
from sqlalchemy import desc
from db_schema.auth_service_models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from db_schema.db_extensions import database

auth = Blueprint("auth",__name__)

API_GATEWAY_URL = "http://localhost:5005"

@auth.route("/register", methods=["POST"])
def register():
    data = request.json
    if Users.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email уже зарегистрирован'}), 400

    hashed_password = generate_password_hash(data["password"],salt_length=128)
    new_user = Users(nickname=data["nickname"],password=hashed_password, email=data["email"],group=data["group"],is_teacher=data["is_teacher"])
    database.session.add(new_user)
    database.session.commit()
    return jsonify({"message": "Пользователь зарегистрирован","user_id":new_user.user_id,"nickname": new_user.nickname,"is_teacher":new_user.is_teacher}), 200


@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    user = Users.query.filter_by(email=data["email"]).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"error": "Неправильный логин или пароль"}), 400
    return jsonify({"message": "Вход выполнен","user_id": user.user_id, "nickname": user.nickname}),200

@auth.route('/get_user_info', methods=['GET'])
def get_user_info():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "Произошла ошибка. Попробуйте позже"}), 400

    user = Users.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({"error": "Произошла ошибка. Попробуйте позже"}), 400

    return jsonify({"message": "Пользователь найден","user_info": user.to_dict()}),200

@auth.route('/get_group_info', methods=['GET'])
def get_group_info():
    group = request.args.get("group")

    if not group:
        return jsonify({"error": "Произошла ошибка. Попробуйте позже"}), 400

    group_info = [user.to_dict() for user in Users.query.filter_by(group=group).order_by(desc(Users.average_score).nullslast()).all()]

    if not group_info:
        return jsonify({"error": "Произошла ошибка. Попробуйте позже"}), 400

    return jsonify({"message": "Пользователь найден","group_info": group_info}),200

@auth.route('/update_average_score', methods=['POST'])
def update_average_score():
    user_id = request.args.get("user_id")
    average_score = request.args.get("average_score")

    if not user_id or not average_score:
        return jsonify({"error": "Произошла ошибка. Попробуйте позже"}), 400

    existing_result = Users.query.filter_by(
        user_id=user_id,
    ).first()

    if not existing_result:
        return jsonify({"error": "Пользователь не найден"}), 400

    existing_result.average_score = average_score
    database.session.commit()

    return jsonify({"message": "Средний результат обновлен"}),200
