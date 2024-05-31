from datetime import datetime
from pytz import timezone

from database import db


class PreviousWorks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String)
    date = db.Column(db.String(100))
    logo_url = db.Column(db.String(1000))
    project_details_url = db.Column(db.String(1000))
    before_url = db.Column(db.String(1000))
    after_url = db.Column(db.String(1000))

    def __init__(self, company_name, logo_url, project_details_url, before_url, after_url):
        self.company_name = company_name
        self.date = datetime.now(timezone('Asia/Dhaka')).strftime("%d %B, %Y")
        self.logo_url = logo_url
        self.project_details_url = project_details_url
        self.before_url = before_url
        self.after_url = after_url

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


