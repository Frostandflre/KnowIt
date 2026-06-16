import time
from datetime import datetime
from flask import Blueprint,render_template,make_response,request,url_for,flash,redirect,session
from .forms import RegistrationForm,AuthorizationForm
import requests

main = Blueprint("main",__name__)

API_GATEWAY_URL = "http://localhost:5005"

@main.route("/")
def main_page():
    nickname = "Guest"
    if 'nickname' in request.cookies:
        nickname = request.cookies.get('nickname')

    return render_template("welcome_page.html",nickname=nickname)

@main.route("/login",methods=['GET', 'POST'])
def login_page():
    nickname = "Guest"
    if 'nickname' in request.cookies:
        nickname = request.cookies.get('nickname')
    form = AuthorizationForm()
    if form.validate_on_submit():
        user_data = {
            'email': form.email.data,
            'password': form.password.data
        }

        login_response = requests.post(f"{API_GATEWAY_URL}/login", json=user_data)

        if login_response.status_code == 400:
            flash("Неправильный email или пароль!", "error")
            return redirect(url_for('main.login_page'))

        if login_response.status_code != 200:
            flash("Ошибка входа. Попробуйте позже.", "error")
            return redirect(url_for('main.login_page'))

        user_info = login_response.json()

        nickname = user_info["nickname"]
        user_id = str(user_info["user_id"])

        save_cookie_response = make_response(redirect(url_for('main.main_page')))
        save_cookie_response.set_cookie('nickname', nickname,max_age=60*60*24*30, secure=True, httponly=True,)
        save_cookie_response.set_cookie('user_id', user_id, max_age=60*60*24*30, secure=True, httponly=True, )
        return save_cookie_response
    return render_template('login_page.html', form=form,nickname=nickname)

@main.route("/logout")
def logout_page():
    logout_response = make_response(redirect(url_for('main.main_page')))
    logout_response.set_cookie('nickname', '', expires=0)
    logout_response.set_cookie('user_id', '', expires=0)
    logout_response.set_cookie('is_teacher', '', expires=0)
    return logout_response

@main.route("/registration",methods=['GET', 'POST'])
def registration_page():
    nickname = "Guest"
    if 'nickname' in request.cookies:
        nickname = request.cookies.get('nickname')
    form = RegistrationForm()
    groups = ["121/125/137", "122/124", "123/138", "131/135", "132/134", "133/136", "141", "142/144", "143/146", "145",
              "151", "152", "153", "155", "221/225", "222/228", "223", "224/226", "231/242", "232/236", "233/238",
              "234", "235", "241", "242/247", "243/248", "244/249", "245", "246", "251", "252", "253", "254", "255",
              "256", "257", "321/322/333", "331/332", "341/342", "351", "421/422", "431/433", "432", "441/443", "442",
              "451", "452", "453", "521/524", "522/534", "531", "532", "533", "551", "552", "553", "541", "542", "543"]

    if form.validate_on_submit():
        user_data = {
            'nickname': form.nickname.data,
            'email': form.email.data,
            'password': form.password.data,
            'special_code': form.teacher_code.data,
            'is_teacher': False,
            'group': form.group.data,
        }

        if user_data["special_code"] ==  "c8B2vmHP5F":
            user_data["is_teacher"] = True
        elif user_data["special_code"] is not None and user_data["special_code"] != "c8B2vmHP5F":
            flash("Неверный специальный код" + user_data["special_code"], "error")
            return render_template("registration_page.html", form=form)

        if user_data["group"] is not None and user_data["group"] not in groups:
            flash("Неверный номер группы,выберите номер из списка", "error")
            return render_template("registration_page.html", form=form)

        registration_response = requests.post(f"{API_GATEWAY_URL}/register", json=user_data)

        if registration_response.status_code == 400:
            flash("Email уже зарегистрирован", "error")
            return render_template("registration_page.html", form=form)

        if registration_response.status_code != 200:
            flash("Ошибка регистрации. Попробуйте позже.", "error")
            return render_template("registration_page.html", form=form)

        user_info = registration_response.json()

        nickname = user_info["nickname"]
        user_id = str(user_info["user_id"])

        if user_info["is_teacher"] is not None and user_info["is_teacher"] is True:
            string_is_teacher = "true"
        else:
            string_is_teacher = "false"

        save_cookie_response = make_response(redirect(url_for('main.main_page')))
        save_cookie_response.set_cookie('nickname', nickname, max_age=60 * 60 * 24 * 30, secure=True, httponly=True, )
        save_cookie_response.set_cookie('user_id', user_id, max_age=60 * 60 * 24 * 30, secure=True, httponly=True, )
        save_cookie_response.set_cookie('is_teacher', string_is_teacher, max_age=60 * 60 * 24 * 30, secure=True, httponly=True, )
        return save_cookie_response
    return render_template("registration_page.html",form=form,nickname=nickname,groups=groups)
@main.route("/tests/<profession>",methods=['GET'])
def tests_main_page(profession):
    nickname = "Guest"
    if 'nickname' in request.cookies:
        nickname = request.cookies.get('nickname')


    get_test_cards_response = requests.get(f"{API_GATEWAY_URL}/get_test_cards",params={"profession":profession})

    test_cards_info = get_test_cards_response.json()
    test_cards = test_cards_info['test_cards']

    if get_test_cards_response.status_code == 404:
        flash("Тесты не найдены", "error")
        return redirect(url_for('main.main_page'))

    if get_test_cards_response.status_code == 200:
        test_cards = get_test_cards_response.json()["test_cards"]

    if get_test_cards_response.status_code != 200:
        flash("Произошла ошибка. Попробуйте позже.", "error")
        return redirect(url_for('main.main_page'))

    return render_template("tests_main_page.html",test_cards=test_cards,nickname=nickname)

@main.route("/test/<test_title>/<question_number>",methods=["GET","POST"])
def test_page(test_title,question_number):
    nickname = "Guest"
    if 'nickname' in request.cookies:
        nickname = request.cookies.get('nickname')

    if "test_data" not in session or session.get("current_test") != test_title:
        get_test_response = requests.get(f"{API_GATEWAY_URL}/get_test", params={"test_title": test_title})
        if get_test_response.status_code == 200:
            session["test_data"] = get_test_response.json()["test"]
            session["current_test"] = test_title
            session["score"] = 0
        else:
            flash("Произошла ошибка. Попробуйте позже.", "error")
            return redirect(url_for('main.main_page'))


    test = session["test_data"]

    if "score" not in session:
        session["score"] = 0

    if request.method == "POST":
        user_answer = int(request.form.get("answer"))
        correct = test[int(question_number)-1]["right_answer"]

        if user_answer == correct:
            session["score"] += 1

        if int(question_number) < len(test[0]):
            return redirect(url_for("main.test_page", question_number=int(question_number) + 1,test_title=test_title))
        else:
            return redirect(url_for("main.results_page",test_title=test_title))

    return render_template("test_page.html",question=test[int(question_number)-1],progress=(int(question_number)  * 10),nickname=nickname)

@main.route("/results/<test_title>")
def results_page(test_title):
    nickname = "Guest"
    if 'nickname' in request.cookies:
        nickname = request.cookies.get('nickname')

    user_id = request.cookies.get("user_id")

    score = session.get("score", 0)
    session.clear()
    total = 10
    percent = (score/total) * 100

    save_results_response = requests.post(f"{API_GATEWAY_URL}/save_results", params={"test_title": test_title,"user_id": user_id, "score": score})

    if save_results_response.status_code != 200:
        flash("Результаты не сохранены. Попробуйте позже.", "error")
        return redirect(url_for('main.main_page'))

    return render_template("results.html",score=score,total=total,percent=percent,test_title=test_title,nickname=nickname)

@main.route("/profile")
def profile_page():
    if 'nickname' not in request.cookies or 'user_id' not in request.cookies:
        flash("Пользователь не найден. Повторите попытку позже", "error")
        return redirect(url_for('main.main_page'))

    current_time = time.time()

    user_id = request.cookies.get("user_id")

    if "cached_user_info" not in session or (current_time - session.get("profile_timestamp", 0) > 300):
        get_user_info_response = requests.get(f"{API_GATEWAY_URL}/get_user_info",params={"user_id":user_id})
        if get_user_info_response.status_code == 200:
            session["cached_user_info"] = get_user_info_response.json()["user_info"]
        else:
            flash("Не удалось получить данные о пользователе. Попробуйте позже.", "error")
            return redirect(url_for('main.profile_page'))

    user_info = session["cached_user_info"]

    created_at_formated = datetime.strptime(user_info['created_at'][:10],"%Y-%m-%d").strftime("%Y-%m-%d")
    days_in_platform = (datetime.now() - datetime.strptime(user_info['created_at'][:10],"%Y-%m-%d")).days + 1

    if "cached_tests_passed" not in session or (current_time - session.get("profile_timestamp", 0) > 300):
        tests_passed_response = requests.get(f"{API_GATEWAY_URL}/get_user_tests_results",params={"user_id":user_id})
        if tests_passed_response.status_code == 200:
            tests_passed_info = tests_passed_response.json()["user_results"]
            session["cached_tests_passed"] = len(tests_passed_info)
        else:
            flash("Не удалось получить данные о пользователе. Попробуйте позже.", "error")
            return redirect(url_for('main.profile_page'))

    tests_passed = session["cached_tests_passed"]

    is_teacher = request.cookies.get("is_teacher")

    if is_teacher == "true":
        group_rating = []
    else:
        if "cached_group_info" not in session or (current_time - session.get("profile_timestamp", 0) > 300):
            group = user_info["group"]
            get_group_info_response = requests.get(f"{API_GATEWAY_URL}/get_group_info",params={"group":group})
            if get_group_info_response.status_code == 200:
                session["cached_group_info"] = get_group_info_response.json()["group_info"]
                session["profile_timestamp"] = current_time
            else:
                flash("Не удалось получить данные о группе. Попробуйте позже.", "error")
                return redirect(url_for('main.profile_page'))

        group_info = session["cached_group_info"]


        group_rating = [
            {
                "user_id": user["user_id"],
                "nickname": user["nickname"],
                "average_score": user["average_score"],
            }

            for user in group_info
        ]

    return render_template("profile_page.html",user_info=user_info,tests_passed=tests_passed,group_rating=group_rating,created_at=created_at_formated,days_in_platform=days_in_platform)
