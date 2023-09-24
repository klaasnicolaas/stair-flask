"""Backend models."""
from datetime import datetime

from app import db


class Sensor(db.Model):
    """Sensor model."""

    __tablename__ = "sensors"
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(50), unique=True)
    ip_address = db.Column(db.String(50), unique=True)
    max_distance = db.Column(db.Integer)
    threshold = db.Column(db.Integer)
    status = db.Column(db.String(50))
    last_update = db.Column(db.DateTime)

    def __init__(
        self,
        client_id: str,
        ip_address: str,
        max_distance: int,
        threshold: int,
        status: str,
        last_update: datetime,
    ) -> None:
        """Initialize Sensor model.

        Args:
        ----
            client_id (str): Sensor client ID
            ip_address (str): Sensor IP address
            max_distance (int): Sensor max distance
            threshold (int): Sensor threshold
            status (str): Sensor status
            last_update (datetime): Sensor last update
        """
        self.client_id = client_id
        self.ip_address = ip_address
        self.max_distance = max_distance
        self.threshold = threshold
        self.status = status
        self.last_update = last_update


class Workout(db.Model):
    """Workout model."""

    __tablename__ = "workouts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(300))
    pros = db.Column(db.JSON, nullable=True)
    cons = db.Column(db.JSON, nullable=True)

    def __init__(self, name: str, description: str, pros: dict = None, cons: dict = None) -> None:
        """Initialize Workout model.

        Args:
        ----
            name (str): Workout name
            description (str): Workout description
            pros (dict): Workout pros
            cons (dict): Workout cons
        """
        self.name = name
        self.description = description
        self.pros = pros
        self.cons = cons
