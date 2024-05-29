import os

from flask import make_response, render_template, request, flash, url_for, redirect
from flask_restful import Resource
from flask_login import login_required, current_user

from models.photography import AlbumDetails
from database import db


class Photography(Resource):
    def get(self):
        album_name_cover = AlbumDetails.query.with_entities(AlbumDetails.album_name,
                                                            AlbumDetails.album_cover_path).all()
        return make_response(render_template('photography.html', album_name_cover=album_name_cover))

    @login_required
    def post(self):
        pass


class CreateAlbum(Resource):
    @login_required
    def get(self):
        return make_response(render_template("create_album.html"))

    @login_required
    def post(self):
        album_details = dict(request.form.items())
        all_album_names = [album_name for (album_name,) in
                           AlbumDetails.query.with_entities(AlbumDetails.album_name).all()]
        if album_details.get('album_name') in all_album_names:
            flash("This album name is already exists. Please choose a new name.")
            return redirect(url_for('createalbum'))
        else:
            uploaded_cover = request.files['album_cover_picture']
            print('uploaded_cover', uploaded_cover)
            if uploaded_cover:
                album_cover_path = AlbumDetails.create_cover_path(album_details.get('album_name'))
                uploaded_cover.save(album_cover_path)
            else:
                album_cover_path = ('https://img.freepik.com/free-vector/blue-computer-folder-flat-style_78370-1029'
                                    '.jpg?size=626&ext=jpg&ga=GA1.1.2130985458.1711371720&semt=ais_user')

            new_album = AlbumDetails(album_name=album_details.get('album_name'),
                                     description=album_details.get('description'),
                                     album_url=album_details.get('album_url'),
                                     album_cover_path=album_cover_path)
            new_album.save_to_db()
            return redirect(url_for('album', album_name=new_album.album_name))


class Album(Resource):
    def get(self, album_name):
        album_details = AlbumDetails.query.filter_by(album_name=album_name).first()
        if album_details:
            photo_urls = AlbumDetails.get_url_of_photos_and_album_name(album_details.album_url)
            return make_response(render_template('album.html', album_details=album_details, photo_urls=photo_urls))
        else:
            flash("There is no album named {}".format(album_name))
            # return make_response(render_template('message.html'))
            return redirect(url_for('home'))

    @login_required
    def post(self, album_name):
        pass


class UpdateAlbum(Resource):
    @login_required
    def get(self, album_name):
        album_details = AlbumDetails.query.filter_by(album_name=album_name).first()
        return make_response(render_template('update_album.html', album_details=album_details))

    def post(self, album_name):
        album_details = dict(request.form.items())

        all_album_names = [album_name for (album_name,) in
                           AlbumDetails.query.with_entities(AlbumDetails.album_name).all()]
        if album_details.get('album_name') in all_album_names:
            flash("This album name is already exists. Please choose a new name.")
            return redirect(url_for('updatealbum', album_name=album_name))

        AlbumDetails.query.filter_by(album_name=album_name).update(album_details)
        db.session.commit()

        if request.files['album_cover_picture']:
            album = AlbumDetails.query.filter_by(album_name=album_details.get('album_name')).first()
            os.remove(album.album_cover_path)
            album.album_cover_path = AlbumDetails.create_cover_path(album_details.get('album_name'))
            db.session.commit()

            uploaded_cover = request.files['album_cover_picture']
            album_cover_path = AlbumDetails.create_cover_path(album_details.get('album_name'))
            uploaded_cover.save(album_cover_path)

        return redirect(url_for('album', album_name=album_details.get('album_name')))
