from flask import make_response, render_template, request, flash, redirect, url_for, jsonify
from flask_restful import Resource
from flask_login import login_required

from models.blogs import Blogs
from database import db


class AllBlogs(Resource):
    def get(self):
        all_blogs = Blogs.query.order_by(Blogs.id.desc()).all()
        total_blogs = len(all_blogs)
        all_categories = set(category for (category,) in Blogs.query.with_entities(Blogs.category).all())
        return make_response(render_template('all_blogs.html', all_blogs=all_blogs,
                                             categories=all_categories, total_blogs=total_blogs))


class CreatePost(Resource):
    @login_required
    def get(self):
        return make_response(render_template("create_post.html"))

    @login_required
    def post(self):
        data = dict(request.form.items())

        new_post = Blogs(title=data.get('title'),
                         description=data.get('description'),
                         category=data.get('category').strip(),
                         cover_path=None)

        new_post.save_to_db()
        new_cover_path = Blogs.create_cover_path(new_post.id)
        uploaded_cover = request.files['cover_picture']
        uploaded_cover.save(new_cover_path)
        new_post.cover_path = new_cover_path
        new_post.save_to_db()

        return redirect(url_for('allblogs'))


class Post(Resource):
    def get(self, post_id):
        post = Blogs.query.filter_by(id=post_id).first()
        return make_response(render_template('post_page.html', post=post))


class UpdatePost(Resource):
    @login_required
    def get(self, post_id):
        blog = Blogs.query.filter_by(id=post_id).first()
        if blog is None:
            flash("No blog found.")
        return make_response(render_template("update_post.html", blog=blog))

    @login_required
    def post(self, post_id):
        data = dict(request.form.items())

        Blogs.query.filter_by(id=data.get('id')).update(data)
        db.session.commit()

        if request.files['cover_picture']:
            cover_path = Blogs.create_cover_path(data.get('id'))
            uploaded_cover = request.files['cover_picture']
            uploaded_cover.save(cover_path)

        return redirect(url_for('post', post_id=data.get('id')))


class LoadMoreBlogs(Resource):
    def get(self):
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 10))
        blogs = Blogs.query.order_by(Blogs.id.desc()).offset(offset).limit(limit).all()
        blogs_data = [{
            'id': blog.id,
            'title': blog.title,
            'category': blog.category,
            'cover_path': blog.cover_path,
            'date': blog.date,
            'description': blog.description,
            'author': blog.author
        } for blog in blogs]
        return jsonify(blogs_data)
