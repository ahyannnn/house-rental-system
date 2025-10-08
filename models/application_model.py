from extensions import db
from datetime import datetime

class Application(db.Model):
    __tablename__ = 'Applications'

    applicationid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    unitID = db.Column(db.Integer, nullable=True)  # nullable for initial state
    status = db.Column(db.String(20), default='Pending')
    submissionDate = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Application {self.email} - {self.status}>"
