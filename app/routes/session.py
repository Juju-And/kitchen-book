from flask import flash, render_template, url_for, redirect, request

from flask_login import logout_user, current_user, login_user

from app.forms import RegistrationForm, LoginForm
from app.models import db, User


def init_routes_session(app):
    @app.route("/register", methods=["GET", "POST"])
    def register():
        try:
            form = RegistrationForm(request.form)

            if request.method == "POST" and form.validate():
                email = form.email.data
                # hashed_password = sha256_crypt.encrypt((str(form.password.data)))

                exists = (
                    db.session.query(User.id).filter_by(email=email).scalar()
                    is not None
                )

                if exists is None:
                    flash("That username is already taken, please choose another")
                    return render_template("register.html", form=form, selected_menu="register")

                else:
                    user = User(email=email)
                    user.set_password(form.password.data)
                    db.session.add(user)
                    db.session.commit()
                    flash(
                        f"Your account has been created! You are now able to log in!",
                        "success",
                    )
                    return redirect(url_for("mainpage"))

            return render_template("register.html", form=form, selected_menu="register")

        except Exception as e:
            return str(e)

    #
    # @app.route("/login", methods=["GET", "POST"])
    # def login():
    #     form = LoginForm()
    #     if form.validate_on_submit():
    #         if form.email.data == "admin@admin.pl" and form.password.data == "password":
    #             flash("You have been logged in!", "success")
    #             return redirect(url_for("mainpage"))
    #         else:
    #             flash("Login Unsuccessful. Please check username and password.")
    #     return render_template("login.html", title="Login", form=form)


