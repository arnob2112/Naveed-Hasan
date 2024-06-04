from flask import Flask
from flask_restful import Api
from flask_login import LoginManager

from database import db
from models.users import Users
from resources.home import Home, Portfolio
from resources.authentication import Login, Logout
from resources.blogs import AllBlogs, CreatePost, Post, UpdatePost, LoadMoreBlogs
from resources.photography import Photography, CreateAlbum, Album, UpdateAlbum
from resources.career import AllBusiness, CreateBusiness
from resources.career import AllCaseStudies, CreateCaseStudy, CaseStudy, UpdateCaseStudy
from resources.career import AllWorks, CreateWork, Work, UpdateWork

app = Flask(__name__)
app.secret_key = "Naveed"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///All Information.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(user_id):
    return Users.query.get(int(user_id))


db.init_app(app)
with app.app_context():
    db.create_all()

api.add_resource(Home, '/')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Portfolio, '/portfolio')
# BLOG SECTION
api.add_resource(AllBlogs, '/all_blogs')
api.add_resource(CreatePost, '/create_post')
api.add_resource(Post, '/post/<string:post_id>')
api.add_resource(UpdatePost, '/update_post/<string:post_id>')
api.add_resource(LoadMoreBlogs, '/load_more_blogs')
# PHOTOGRAPHY SECTION
api.add_resource(Photography, '/photography')
api.add_resource(CreateAlbum, '/photography/create_new_album')
api.add_resource(Album, '/photography/album/<string:album_name>')
api.add_resource(UpdateAlbum, '/photography/album/<string:album_name>/update_album')
# BUSINESS SECTION
api.add_resource(AllBusiness, '/career/business/all')
api.add_resource(CreateBusiness, '/career/business/create')
# CASE STUDY SECTION
api.add_resource(AllCaseStudies, '/career/case_study/all')
api.add_resource(CreateCaseStudy, '/career/case_study/create')
api.add_resource(CaseStudy, '/career/case_study/<string:case_id>')
api.add_resource(UpdateCaseStudy, '/career/case_study/update/<string:case_id>')
# PREVIOUS WORK SECTION
api.add_resource(AllWorks, '/career/previous_works/all')
api.add_resource(CreateWork, '/career/previous_works/create')
api.add_resource(Work, '/career/previous_works/<string:work_id>')
api.add_resource(UpdateWork, '/career/previous_works/update/<string:work_id>')


if __name__ == "__main__":
    app.run(port=5000, debug=True)
