from flask import make_response, render_template, request, flash, redirect, url_for
from flask_restful import Resource
from flask_login import login_required, current_user
import requests

from models.case_study import CaseStudies
from database import db


class AllCaseStudies(Resource):
    def get(self):
        all_case_studies = CaseStudies.query.all()[::-1]
        all_categories = set(category for (category,) in CaseStudies.query.with_entities(CaseStudies.category).all())
        if not bool(all_case_studies):
            flash("No case study available.")
        return make_response(render_template('all_case_studies.html',
                                             all_case_studies=all_case_studies, categories=all_categories))


class CreateCaseStudy(Resource):
    @login_required
    def get(self):
        return make_response(render_template("create_case_study.html"))

    @login_required
    def post(self):
        data = dict(request.form.items())

        new_case = CaseStudies(title=data.get('title'),
                               description=data.get('description'),
                               category=data.get('category').strip(),
                               pdf_path=CaseStudies.convert_drive_link(data.get('pdf_path')),
                               cover_path=None)

        new_case.save_to_db()

        new_cover_path = CaseStudies.create_cover_path(new_case.id)
        uploaded_cover = request.files['cover_picture']
        uploaded_cover.save(new_cover_path)
        new_case.cover_path = new_cover_path
        new_case.save_to_db()

        return redirect(url_for('allcasestudies'))


class CaseStudy(Resource):
    def get(self, case_id):
        case_study = CaseStudies.query.filter_by(id=case_id).first()
        return make_response(render_template('case_study_page.html', case_study=case_study))


class UpdateCaseStudy(Resource):
    @login_required
    def get(self, case_id):
        case_study = CaseStudies.query.filter_by(id=case_id).first()
        if case_study is None:
            flash("No case study found.")
        return make_response(render_template("update_case_study.html", case_study=case_study))

    @login_required
    def post(self, case_id):
        data = dict(request.form.items())

        CaseStudies.query.filter_by(id=data.get('id')).update(data)
        db.session.commit()

        if request.files['cover_picture']:
            cover_path = CaseStudies.create_cover_path(data.get('id'))
            uploaded_cover = request.files['cover_picture']
            uploaded_cover.save(cover_path)

        return redirect(url_for('casestudy', case_id=data.get('id')))
