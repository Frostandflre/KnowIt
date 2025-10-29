from flask import Blueprint,render_template,make_response,request

main = Blueprint("main",__name__)

API_GATEWAY_URL = "http://localhost:5005"

@main.route("/")
def main_page():
    nickname = "Guest"
    if 'nickname' in request.cookies:
        nickname = request.cookies.get('nickname')

    return render_template("main_page.html",nickname = nickname)