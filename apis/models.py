from flask import request
import flask
from flask import jsonify
import flask.ext.sqlalchemy
import flask.ext.restless
from apis.connection import db

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)

    def __init__(self, name):
        self.name = name

db.create_all()
