from extensions import db


class Company(db.Model):

    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    company_name = db.Column(db.String(200))

    hr_contact = db.Column(db.String(100))

    website = db.Column(db.String(200))

    approval_status = db.Column(db.String(20), default="pending")

    is_blacklisted = db.Column(db.Boolean, default=False)

    drives = db.relationship("Drive", backref="company")