from flask import make_response, render_template, request, flash, url_for, redirect
from flask_restful import Resource
from flask_login import login_required, current_user

from models.photography import AlbumDetails


class Photography(Resource):
    def get(self):
        album_names = AlbumDetails.query.with_entities(AlbumDetails.album_name).all()
        return make_response(render_template('photography.html', album_names=album_names))

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
        all_album_names = [album_name for (album_name,) in AlbumDetails.query.with_entities(AlbumDetails.album_name).all()]
        if album_details.get('album_name') in all_album_names:
            flash("This album name is already exists. Please choose a new name.")
            return redirect(url_for('createalbum'))
        else:
            new_album = AlbumDetails(album_name=album_details.get('album_name'),
                                     description=album_details.get('description'),
                                     album_url=album_details.get('album_url'))
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
