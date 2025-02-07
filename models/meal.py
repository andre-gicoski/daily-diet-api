
from database import db
from datetime import datetime, timezone

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(100), nullable=False) 
    description = db.Column(db.Text, nullable=True) 
    date_time = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    within_diet = db.Column(db.Boolean, nullable=False) 
