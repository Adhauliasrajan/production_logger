from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Production(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    machine_id = db.Column(db.String(20), nullable=False)
    shift = db.Column(db.String(10), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    units = db.Column(db.Integer, nullable=False)
    uptime_hrs = db.Column(db.Float, nullable=False)
    downtime = db.Column(db.Float, nullable=False)
