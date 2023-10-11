"""Authentication user models."""
# ruff: noqa: A003
from __future__ import annotations

from typing import TYPE_CHECKING

from flask import flash, redirect, url_for
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login
from app.const import IsAdmin

if TYPE_CHECKING:
    from datetime import datetime


@login.unauthorized_handler
def unauthorized() -> None:
    """Redirect unauthorized users to Login page."""
    flash("You must be logged in to view that page.")
    return redirect(url_for("auth.login"))


class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, index=False, nullable=False)

    def __init__(
        self,
        name: str,
        email: str,
        password: str,
        is_admin: IsAdmin = IsAdmin.NO.value,
        created_at: datetime | None = None,
    ) -> None:
        """Initialize the user."""
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password, method="scrypt")
        self.is_admin = is_admin
        self.created_at = created_at

    def set_password(self, password: str) -> None:
        """Set password.

        Args:
        ----
            password (str): The password to set.
        """
        self.password_hash = generate_password_hash(password, method="scrypt")

    def check_password(self, password: str) -> bool:
        """Check password.

        Args:
        ----
            password (str): The password to check.
        """
        return check_password_hash(self.password_hash, password)
