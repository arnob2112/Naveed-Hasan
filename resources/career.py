from flask import make_response, render_template, request, flash, redirect, url_for
from flask_restful import Resource
from flask_login import login_required

from models.business import Business
from models.case_study import CaseStudies
from models.previous_works import PreviousWorks
from database import db


class AllBusiness(Resource):
    def get(self):
        all_business = Business.query.all()[::-1]
        if not bool(all_business):
            flash("No business available.")
            return redirect(url_for('home'))
        return make_response(render_template('all_business.html', all_business=all_business))


class CreateBusiness(Resource):
    @login_required
    def get(self):
        return make_response(render_template("create_business.html"))

    @login_required
    def post(self):
        data = dict(request.form.items())

        new_business = Business(company_name=data.get('company_name'),
                                logo_url=data.get('logo_url'),
                                business_url=data.get('business_url'), )
        new_business.save_to_db()
        return redirect(url_for('allbusiness'))


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
            return redirect(url_for('allcasestudy'))
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


class AllWorks(Resource):
    def get(self):
        all_works = PreviousWorks.query.all()[::-1]
        if not bool(all_works):
            flash("No previous works available.")
            return redirect(url_for('home'))
        return make_response(render_template('all_works.html', all_works=all_works))


class CreateWork(Resource):
    @login_required
    def get(self):
        return make_response(render_template("create_work.html"))

    @login_required
    def post(self):
        data = dict(request.form.items())

        new_work = PreviousWorks(company_name=data.get('company_name'),
                                 logo_url=data.get('logo_url'),
                                 project_details_url=data.get('project_details_url'),
                                 before_url=data.get('before_url'),
                                 after_url=data.get('after_url'))
        new_work.save_to_db()
        return redirect(url_for('allworks'))


class Work(Resource):
    def get(self, work_id):
        work = PreviousWorks.query.filter_by(id=work_id).first()
        return make_response(render_template('work_page.html', work=work))


class UpdateWork(Resource):
    @login_required
    def get(self, work_id):
        work = PreviousWorks.query.filter_by(id=work_id).first()
        if work is None:
            flash("No previous work found.")
            return redirect(url_for('allworks'))
        return make_response(render_template("update_work.html", work=work))

    @login_required
    def post(self, work_id):
        data = dict(request.form.items())

        PreviousWorks.query.filter_by(id=data.get('id')).update(data)
        db.session.commit()
        return redirect(url_for('work', work_id=data.get('id')))
