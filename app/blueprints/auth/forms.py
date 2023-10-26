"""Forms for user authentication."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    """Login form class."""

    email = StringField(
        "E-mail",
        validators=[DataRequired(), Email(message="Vul een geldig e-mailadres in.")],
    )
    password = PasswordField("Wachtwoord", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    """Registration form class."""

    name = StringField("Naam", validators=[DataRequired()])
    email = StringField(
        "E-mail",
        validators=[DataRequired(), Email(message="Vul een geldig e-mailadres in.")],
    )
    password = PasswordField(
        "Wachtwoord",
        validators=[
            DataRequired(),
            Length(
                min=6,
                message="Zorg ervoor dat uw wachtwoord minimaal 6 tekens lang is.",
            ),
        ],
    )
    confirm = PasswordField(
        "Bevestig Wachtwoord",
        validators=[
            DataRequired(),
            EqualTo("password", message="Wachtwoorden moeten overeenkomen."),
        ],
    )
