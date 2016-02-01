from flask import request
import flask
from flask import jsonify
import flask.ext.sqlalchemy
import flask.ext.restless
from apis.connection import db
from sqlalchemy.dialects.mysql import DOUBLE


def _get_date():
    return datetime.datetime.now()

"""
class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)

    def __init__(self, name):
        self.name = name
"""

class Videos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prodCost = db.Column(DOUBLE)
    producedOn = db.Column(db.Date, default=_get_date)


class FBVideos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    videoId = db.Column(db.Integer, ForeignKey("Videos.id"), nullable=False)
    publishedOn = db.Column(db.Date, default=_get_date)


class YTVideos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    videoId = db.Column(db.Integer, ForeignKey("Videos.id"), nullable=False)
    publishedOn = db.Column(db.Date, default=_get_date)


db.create_all()
