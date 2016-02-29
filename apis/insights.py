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
    r = youtube_get_insights(video_ids)
    r = flask.Response(r)
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r

if __name__ == "__main__":
    app.run(host="0.0.0.0")
