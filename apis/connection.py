from flask import request
import flask
from flask import jsonify
import flask.ext.sqlalchemy
import flask.ext.restless
import json
from sqlalchemy.sql import text
from _mysql_exceptions import IntegrityError

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/glamrscms'
db = flask.ext.sqlalchemy.SQLAlchemy(app)

