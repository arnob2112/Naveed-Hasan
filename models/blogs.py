from datetime import datetime
from pytz import timezone
from werkzeug.utils import secure_filename
import os

from database import db


class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    date = db.Column(db.String(100))
    category = db.Column(db.String(100))
    author = db.Column(db.String(100))
    cover_path = db.Column(db.String(1000))

    def __init__(self, title, description, category, cover_path):
        self.title = title
        self.description = description
        self.date = datetime.now(timezone('Asia/Dhaka')).strftime("%d %B, %Y")
        self.category = category
        self.author = "Naveed Hasan"
        self.cover_path = cover_path

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def create_cover_path(blog_id):
        upload_folder = os.path.join('static', 'blog_covers')
        image_filename = secure_filename('cover-' + str(blog_id) + ".jpg")
        image_path = os.path.join(upload_folder, image_filename)
        return image_path

