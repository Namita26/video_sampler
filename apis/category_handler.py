from flask import request
import flask
from flask import jsonify
import flask.ext.sqlalchemy
import flask.ext.restless
import json
from sqlalchemy.sql import text


app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/glamrscms'
db = flask.ext.sqlalchemy.SQLAlchemy(app)


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)

    def __init__(self, name):
        self.name = name

# db.create_all()


@app.route('/category/', methods = ['GET'])
def index():
    """
    Index all the categories present in database.
    """
    cats = []
    result = db.engine.execute("select * from categories")
    for i in result:
        cats.append({"id":i["id"], "name":i["name"]})
    cats_json = json.dumps({"categories":cats})
    return cats_json


@app.route('/category/<int:id>/', methods = ['GET'])
def get_category(id):
    """
    Return the category info for input id
    :param id: database id of the category
    """
    val = id
    cat = db.session.execute('select * from categories where id = :id', {'id': val})
    for i in cat:
        cat_name = i.name
        cat_id = i.id
    data = json.dumps([{"id": cat_id, "name": cat_name}], indent=4)
    return data


@app.route('/category/', methods = ['POST'])
def create_category():
    """
    Create/register a new category in the database
    POST request
    """
    inputs = {'id': request.json.get('id'), 'name': request.json.get(u'name')}
    new_cat = db.session.execute(text(""" insert into categories (id, name) values (:id, :name) """), inputs)
    db.session.commit()
    return "added successfully"


@app.route('/category/<int:id>/', methods = ['DELETE'])
def delete_category_by_id(id):
    """
    Deletes a category from the database by input id
    :param id: database id of the category

    """
    val = id
    cat = db.session.execute('delete from categories where id = :id', {'id': val})
    db.session.commit()
    return jsonify({'result': True})


@app.route('/category/<int:id>/', methods = ['PUT'])
def update_category_by_id(id):
    """
    Updates category info in database for input id
    :param id: database id of the category
    """
    inputs = {'id': id, 'name': request.json.get(u'name')}
    cat = db.session.execute('update categories set name= :name where id= :id', {'id': inputs['id'], 'name': inputs['name']})
    db.session.commit()
    return jsonify({"result": True})


if __name__ == "__main__":
    app.run()
