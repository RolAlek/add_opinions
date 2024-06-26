from datetime import datetime

from . import db


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    create_date = db.Column(db.DateTime, index=True, default=datetime.now)
    added_by = db.Column(db.String(64))
