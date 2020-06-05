from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    SelectField,
    TextAreaField,
    FileField,
)
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign up")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")
    remember_me = BooleanField("Remember Me")


class AddProductFrom(FlaskForm):
    name = StringField("Name")
    category = SelectField("Category")


class AddRecipeFrom(FlaskForm):
    name = StringField("Name")
    method = TextAreaField("How to make it")
    preparation_time = StringField("Time")
    picture = FileField("Image File")
                        # [validators.regexp("^[^/\\]\.jpg$")])
    ingredient = SelectField("Product")
    # ingredient2 = SelectField("Product")
    # ingredient3 = SelectField("Product")
