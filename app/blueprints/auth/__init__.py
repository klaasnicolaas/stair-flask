"""Blueprint for the authentication pages."""
from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import db

from .forms import LoginForm, RegisterForm
from .models import User

bp = Blueprint("auth", __name__, template_folder="templates")


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Render the login page.

    Returns
    -------
        render_template: The login page.
    """
    if current_user.is_authenticated:
        return redirect(url_for("backend.dashboard"))
    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(password=form.password.data):
            login_user(user)
            flash("Welcome back!", "info")
            return redirect(url_for("backend.dashboard"))
        flash("Please check your login details and try again", "danger")
        return redirect(url_for("auth.login"))
    return render_template("login.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register() -> None:
    """Render the register page.

    Returns
    -------
        render_template: The register page.
    """
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(
                name=form.name.data,
                email=form.email.data,
                password=form.password.data,
                created_at=datetime.now(),
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("backend.dashboard"))
        flash("A user already exists with that email address.", "danger")
    return render_template("register.html", form=form)


@bp.route("/forgot-password", methods=["GET"])
def forgot_password() -> None:
    """Render the forgot password page."""
    return "forgot password"


@bp.route("/reset-password", methods=["GET"])
def reset_password() -> None:
    """Render the reset password page."""
    return "reset password"


@bp.route("/logout")
@login_required
def logout() -> None:
    """Render the logout page.

    Returns
    -------
        redirect: The home page.
    """
    logout_user()
    return redirect(url_for("frontend.home"))
