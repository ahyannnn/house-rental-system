from extensions import db  # ✅ use this instead of from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'Users'

    userid = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), default='Tenant')  # Default role is 'Tenant'
    datecreated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.email}>"
