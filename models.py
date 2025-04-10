from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ResumeHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120))
    predicted_category = db.Column(db.String(100))
    selected_category = db.Column(db.String(100))
    fit = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
