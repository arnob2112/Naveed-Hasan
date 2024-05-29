from datetime import datetime
from pytz import timezone
from werkzeug.utils import secure_filename
import os

from database import db


class CaseStudies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    date = db.Column(db.String(100))
    category = db.Column(db.String(100))
    pdf_path = db.Column(db.String(1000))
    cover_path = db.Column(db.String(1000))

    def __init__(self, title, description, category, pdf_path, cover_path):
        self.title = title
        self.description = description
        self.date = datetime.now(timezone('Asia/Dhaka')).strftime("%d %B, %Y")
        self.category = category
        self.pdf_path = pdf_path
        self.cover_path = cover_path

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def create_cover_path(case_study_id):
        upload_folder = os.path.join('static', 'case_study_covers')
        image_filename = secure_filename('case study-' + str(case_study_id) + ".jpg")
        image_path = os.path.join(upload_folder, image_filename)
        return image_path

    @staticmethod
    def convert_drive_link(view_link):
        if "drive.google.com/file/d/" in view_link:
            file_id = view_link.split('/')[5]
            embedded_link = f"https://drive.google.com/file/d/{file_id}/preview"
            return embedded_link
        else:
            # raise ValueError("Invalid Google Drive view link format.")
            return None
