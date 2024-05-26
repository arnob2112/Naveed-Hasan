from flask import render_template, make_response, request, flash
from flask_restful import Resource
import requests


class Home(Resource):

    def get(self):
        return make_response(render_template("base.html"))
