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
from social_handles_data.utils.fb import get_insights as facebook_get_insights
from social_handles_data.utils.yt import get_insights as youtube_get_insights
from social_handles_data import youtube_data
from social_handles_data import fb_yt_studio_videos, fb_yt_stats
import datetime
import requests


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


@app.route('/fb_yt_titles/', methods = ['GET'])
def get_fb_titles():
    fb_video_ids = ["319863888091100_871392976271519", "319863888091100_935940949816721", "319863888091100_925173684226781", "319863888091100_929871233757026", "319863888091100_947482865329196", "319863888091100_898908596853290", "319863888091100_851685721575578"]
    yt_video_ids = ["-7MV-cspVXM", "4pNKgsvyEdw", "DRoNTDRJNuU", "J5xNIJlfBAw", "NlDWRmDCa_o", "pEn0H-R-YnU", "ubePCsGXcUE"]

    all_fb_titles = []
    all_yt_titles = []

    for video_id in fb_video_ids:
        id_title_map = {}
        title = facebook_data.get_video_title(video_id)
        id_title_map["video_id"] = video_id
        id_title_map["video_title"] = title
        all_fb_titles.append(id_title_map)


    for video_id in yt_video_ids:
        id_title_map = {}
        title = youtube_data.get_video_title(video_id)
        id_title_map["video_id"] = video_id
        id_title_map["video_title"] = title
        all_yt_titles.append(id_title_map)

    r = json.dumps({"facebook": all_fb_titles, "youtube": all_yt_titles})
    r = flask.Response(r)
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r


@app.route('/yt_embed/', methods = ['GET'])
def get_yt_embed_link():
    link = request.args.get("link")
    result = requests.get("https://www.youtube.com/oembed?url="+link)
    embeded_link = "<link>" + result.json()['html'] + "</link>"
    dict1 = {"embeded_link": embeded_link}
    r = json.dumps(dict1)
    r = flask.Response(r)
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r


@app.route('/fb_embed/', methods = ['GET'])
def get_fb_embed_link():
    video_id = request.args.get("video_id")
    result = requests.get("https://www.facebook.com/plugins/video/oembed.json/?url=https://www.facebook.com/ClubGlamrs/posts/"+video_id)
    embeded_link = str(result.json()['html']).replace("\n", "")
    
    dict1 = {"embeded_link": embeded_link}
    r = json.dumps(dict1)
    r = flask.Response(r)
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r


@app.route('/get_video_ids/', methods = ['GET'])
def get_video_ids():
    r = facebook_data.get_video_ids()
    r = flask.Response(r)
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r


@app.route('/fans_timeline/', methods = ['GET'])
def fb_fans_timeline():
    """
    """
    since = request.args.get('since')
    until = request.args.get('until')
    r = facebook_data.get_fans_timeline_data(since, until)
    r = flask.Response(r)
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r


@app.route('/gain_to_loss/', methods = ['GET'])
def gain_to_loss():
    """
    """
    since = request.args.get('since')
    until = request.args.get('until')
    r = facebook_data.get_gain_loss_fans_data(since, until)
    r = flask.Response(r)
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r


@app.route('/page_like_sources/', methods = ['GET'])
def page_like_sources():
    """
    """
    since = request.args.get('since')
    until = request.args.get('until')
    r = facebook_data.page_like_by_sources(since, until)
    r = flask.Response(r)
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r

@app.route('/age_gender/', methods = ['GET'])
def page_age_gender():
    """
    """
    since = request.args.get('since')
    until = request.args.get('until')
    r = facebook_data.page_gender_and_age_group_fans(since, until)
    r = flask.Response(r)
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r


@app.route('/countrywise_fans/', methods = ['GET'])
def page_countrywise_fans():
    """
    """
    since = request.args.get('since')
    until = request.args.get('until')
    r = facebook_data.page_country_wise_fans(since, until)
    r = flask.Response(r)
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r


@app.route('/citywise_fans/', methods = ['GET'])
def page_citywise_fans():
    """
    """
    since = request.args.get('since')
    until = request.args.get('until')
    r = facebook_data.page_city_wise_fans(since, until)
    r = flask.Response(r)
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r


@app.route('/page_reach/', methods = ['GET'])
def page_reach():
    """
    """
    since = request.args.get('since')
    until = request.args.get('until')
    r = facebook_data.page_reach(since, until)
    r = flask.Response(r)
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r


@app.route('/page_impressions/', methods = ['GET'])
def page_impressions():
    """
    """
    since = request.args.get('since')
    until = request.args.get('until')
    r = facebook_data.page_impressions(since, until)
    r = flask.Response(r)
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r


@app.route('/page_performance/', methods = ['GET'])
def page_performance():
    """
    """
    since = request.args.get('since')
    until = request.args.get('until')
    r = facebook_data.page_performance(since, until)
    r = flask.Response(r)
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r


@app.route('/page_negative/', methods = ['GET'])
def page_negative():
    """
    """
    since = request.args.get('since')
    until = request.args.get('until')
    r = facebook_data.page_negative_feedback(since, until)
    r = flask.Response(r)
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r

def convert_to_epoch_timestamp(datestring):
    time_format = "%Y-%m-%d %H:%M:%S"
    start_date = datetime.datetime.strptime(datestring, time_format)
    timestamp = (start_date - datetime.datetime(1970, 1, 1)).total_seconds()
    return timestamp
    

@app.route('/page_insights/', methods = ['GET'])
def fb_all_graphs_data():
    """
    Fetch Insights object and return 
    """
    since_date = request.args.get('since')
    until_date = request.args.get('until')
    since = convert_to_epoch_timestamp(since_date + ' 08:00:00')
    until = convert_to_epoch_timestamp(until_date + ' 08:00:00')
    r = facebook_data.page_insights(since, until)
    r = flask.Response(r)
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r


@app.route('/fb_yt/', methods = ['GET'])
def fb_yt():
    """
    Fetch Facebook and YouTube views, likes, comments, shares
    : Output: return all desired values for a array of video ids.
    """
    if request.args.get('ids'):
        video_ids = request.args.get('ids')
        data = json.loads(str(video_ids.split("=")[1]))
        r = fb_yt_stats.fetch_data(data)
    else:
        r = fb_yt_stats.chart_details()
    r = flask.Response(r)
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r


@app.route('/facebook_insights/', methods = ['GET'])
def fb_insights():
    """
    Fetch Facebook insights for input video ids and store in json.
    """
    video_ids = request.args.get('ids')
    r = facebook_get_insights(video_ids)
    r = flask.Response(r)
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r

@app.route('/youtube_insights/', methods = ['GET'])
def yt_insights():
    """
    Fetch YouTube insights for input video ids and store in json.
    """
    video_ids = request.args.get('ids')
    print type(video_ids), "\n=-------------------------\n"
    r = youtube_get_insights(video_ids)
    r = flask.Response(r)
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
