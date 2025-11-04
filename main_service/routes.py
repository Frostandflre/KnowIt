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
    return logout_response

@main.route("/registration",methods=['GET', 'POST'])
def registration_page():
    nickname = "Guest"
    if 'nickname' in request.cookies:
        nickname = request.cookies.get('nickname')
    form = RegistrationForm()
    if form.validate_on_submit():
        user_data = {
            'nickname': form.nickname.data,
            'email': form.email.data,
            'password': form.password.data
        }

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

        save_cookie_response = make_response(redirect(url_for('main.main_page')))
        save_cookie_response.set_cookie('nickname', nickname, max_age=60 * 60 * 24 * 30, secure=True, httponly=True, )
        save_cookie_response.set_cookie('user_id', user_id, max_age=60 * 60 * 24 * 30, secure=True, httponly=True, )
        return save_cookie_response
    return render_template("registration_page.html",form=form,nickname=nickname)

@main.route("/tests/<profession>",methods=['GET'])
def tests_main_page(profession):
    nickname = "Guest"
    if 'nickname' in request.cookies:
        nickname = request.cookies.get('nickname')

    get_test_cards_response = requests.get(f"{API_GATEWAY_URL}/get_test_cards",params={"profession":profession})

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

    get_test_response = requests.get(f"{API_GATEWAY_URL}/get_test",params={"test_title":test_title})

    if get_test_response.status_code == 404:
        flash("Тест не найден", "error")
        return redirect(url_for('main.main_page'))

    if get_test_response.status_code == 200:
        test = get_test_response.json()["test"]

    if get_test_response.status_code != 200:
        flash("Произошла ошибка. Попробуйте позже.", "error")
        return redirect(url_for('main.main_page'))

    if "score" not in session:
        session["score"] = 0

    if request.method == "POST":
        user_answer = int(request.form.get("answer"))
        correct = test[0][int(question_number)-1]["right_answer"]

        if user_answer == correct:
            session["score"] += 1

        if int(question_number) < len(test[0]):
            return redirect(url_for("main.test_page", question_number=int(question_number) + 1,test_title=test_title))
        else:
            return redirect(url_for("main.results_page",test_title=test_title))

    return render_template("test_page.html",question=test[0][int(question_number)-1],progress=(int(question_number)  * 10),nickname=nickname)

@main.route("/results/<test_title>")
def results_page(test_title):
    nickname = "Guest"
    if 'nickname' in request.cookies:
        nickname = request.cookies.get('nickname')

    score = session.get("score", 0)
    session.clear()
    total = 10
    percent = (score/total) * 100
    return render_template("results.html",score=score,total=total,percent=percent,test_title=test_title,nickname=nickname)