from flask import request
import flask
from flask import jsonify
import flask.ext.sqlalchemy
import flask.ext.restless
import json
from sqlalchemy.sql import text
from _mysql_exceptions import IntegrityError
from apis.connection import db, app
from social_handles_data import facebook_data
from social_handles_data import youtube_data


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
    data = json.dumps([{"id": cat_id, "name": cat_name}])
    data = {"category": data}
    return jsonify(data)


@app.route('/category/', methods = ['POST'])
def create_category():
    """
    Create/register a new category in the database
    POST request
    """
    try:
        max_id = None
        if request.json.get('id') == None:
            highest_id = db.engine.execute("select max(id) from categories")
            for val in highest_id:
                max_id = val
                max_id = int(max_id[0])
            inputs = {'id': max_id + 1, 'name': request.json.get(u'name')}
            new_cat = db.session.execute(text(""" insert into categories (id, name) values (:id, :name) """), inputs)
        else:
            inputs = {'id': request.json.get('id'), 'name': request.json.get(u'name')}
            new_cat = db.session.execute(text(""" insert into categories (id, name) values (:id, :name) """), inputs)
        db.session.commit()
        return jsonify({"new_category": inputs, "errorCode": 201}), 201
    except:
        print "In except-----"
        return jsonify({"errorMessage": "record already present"})


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

@app.route('/graph_fb/<string:id>', methods = ['GET'])
def fb_data(id):
    r = facebook_data.fetch_data(id)
    r = flask.Response(r)
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r

@app.route('/graph_yt/<string:id>', methods = ['GET'])
def yt_data(id):
    r = youtube_data.fetch_data(id)
    r = flask.Response(r)
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r


@app.route('/get_video_ids/', methods = ['GET'])
def get_video_ids():
    r = facebook_data.get_video_ids()
    r = flask.Response(r)
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r


if __name__ == "__main__":
    app.run()
