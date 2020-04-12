from flask import flash, render_template, url_for, redirect

from app import app
from app.database import init_db
from app.forms import RegistrationForm, LoginForm

def init_routes_session(app):
    @app.route("/register", methods=["GET", "POST"])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            flash(f"Account created for {form.username.data}!", "success")
            return redirect(url_for("mainpage"))
        return render_template("register.html", title="Register", form=form)


    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            if form.email.data == "admin@admin.pl" and form.password.data == "password":
                flash("You have been logged in!", "success")
                return redirect(url_for("mainpage"))
            else:
                flash("Login Unsuccessful. Please check username and password.")
        return render_template("login.html", title="Login", form=form)
