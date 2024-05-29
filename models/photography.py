from datetime import datetime
from pytz import timezone
import requests
from bs4 import BeautifulSoup
import re
from werkzeug.utils import secure_filename
import os

from database import db


class AlbumDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    album_name = db.Column(db.String, unique=True)
    description = db.Column(db.String(1000))
    album_url = db.Column(db.String(1000))
    album_cover_path = db.Column(db.String(1000))

    def __init__(self, album_name, description, album_url, album_cover_path):
        self.date = datetime.now(timezone('Asia/Dhaka')).strftime("%d %B, %Y")
        self.album_name = album_name
        self.description = description
        self.album_url = album_url
        self.album_cover_path = album_cover_path

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def create_cover_path(album_name):
        upload_folder = os.path.join('static', 'album_covers')
        image_filename = secure_filename(album_name + ".jpg")
        image_path = os.path.join(upload_folder, image_filename)
        return image_path

    @staticmethod
    def get_url_of_photos_and_album_name(album_url):
        response = requests.get(album_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract album name
            album_name_tag = soup.find('meta', property='og:title')
            album_name = album_name_tag['content'] if album_name_tag else 'Unnamed Album'

            # Extract image URLs
            images = soup.find_all('img')
            photo_urls = []
            for img in images:
                if 'src' in img.attrs:
                    src = img['src']
                    # Modify the URL to get full-size images
                    full_size_src = re.sub(r'=w\d+-h\d+-.*', '=w2400', src)
                    photo_urls.append(full_size_src)

            # return album_name, photo_urls[1:]
            return photo_urls[1:]
        else:
            print(f"Failed to retrieve the album. Status code: {response.status_code}")
            return None, []
