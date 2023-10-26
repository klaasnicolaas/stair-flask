"""Forms for the backend."""
from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired


class AddSensorForm(FlaskForm):
    """Add sensor class."""

    client_id = IntegerField("Client ID", validators=[DataRequired()])
    ip_address = StringField("IP Address", validators=[DataRequired()])
