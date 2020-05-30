from flask_login import current_user, login_user, logout_user, LoginManager
from werkzeug.utils import redirect

import app.routes.session
from flask import request, render_template, Response, Flask, url_for, flash

from app.database import init_db
from app.forms import LoginForm
from app.models import User
from app.routes import init_routes

app = Flask(__name__)
init_db(app)
init_routes(app)

FLASK_APP = "app"

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/", methods=["GET"])
def mainpage():
    if request.method == "GET":
        return render_template("main.html", selected_menu="home")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("mainpage"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid email or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("mainpage"))
    return render_template("login.html", title="Sign In", form=form, selected_menu="login")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("mainpage"))


app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run()
