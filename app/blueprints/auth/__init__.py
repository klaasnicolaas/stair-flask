"""The auth blueprint."""
from flask import Blueprint, render_template

bp = Blueprint("auth", __name__, template_folder="templates")

@bp.route("/login", methods=["GET"])
def login() -> None:
    """The login page."""
    return render_template("login.html")