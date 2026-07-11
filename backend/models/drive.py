from extensions import db
from datetime import datetime


class Drive(db.Model):

    __tablename__ = "drives"

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"))

    job_title = db.Column(db.String(200))

    job_description = db.Column(db.Text)

    eligibility_branch = db.Column(db.String(100))

    eligibility_cgpa = db.Column(db.Float)

    eligibility_year = db.Column(db.Integer)

    deadline = db.Column(db.Date)

    status = db.Column(db.String(20), default="pending")
    # pending / approved / closed

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship("Application", backref="drive")