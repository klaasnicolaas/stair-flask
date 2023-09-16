"""Backend models."""
from datetime import datetime

from app import db


class Sensor(db.Model):
    """Sensor model."""

    __tablename__ = "sensors"
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(50), unique=True)
    ip_address = db.Column(db.String(50), unique=True)
    status = db.Column(db.String(50))
    last_update = db.Column(db.DateTime)

    def __init__(
        self,
        client_id: str,
        ip_address: str,
        status: str,
        last_update: datetime,
    ) -> None:
        """Initialize Sensor model.

        Args:
        ----
            client_id (str): Sensor client ID
            ip_address (str): Sensor IP address
            status (str): Sensor status
            last_update (datetime): Sensor last update
        """
        self.client_id = client_id
        self.ip_address = ip_address
        self.status = status
        self.last_update = last_update
