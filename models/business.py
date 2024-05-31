from database import db


class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String)
    logo_url = db.Column(db.String(1000))
    business_url = db.Column(db.String(1000))

    def __init__(self, company_name, logo_url, business_url):
        self.company_name = company_name
        self.logo_url = logo_url
        self.business_url = business_url

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()