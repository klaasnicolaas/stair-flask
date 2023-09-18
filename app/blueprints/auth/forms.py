"""Forms for user authentication."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Enter a valid email.")],
    )
    password = PasswordField("Password", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Enter a valid email.")],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(
                min=6,
                message="Make sure your password is at least 6 characters long.",
            ),
        ],
    )
    confirm = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
