"""Backend models."""
from app import db


class Sensor(db.Model):
    __tablename__ = "sensors"
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(50), unique=True)
    ip_address = db.Column(db.String(50), unique=True)
    status = db.Column(db.String(50))
    last_update = db.Column(db.DateTime)

    def __init__(self, client_id, ip_address, status, last_update):
        self.client_id = client_id
        self.ip_address = ip_address
        self.status = status
        self.last_update = last_update
