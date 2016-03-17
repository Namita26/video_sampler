import requests
import json
import facebook
import datetime
import os
from social_handles_data.utils.file_util import FileUtil

def facebook_graph_object():
    return facebook.GraphAPI(access_token='CAAGYi3qeYAIBAOsFnZCg7SZACH9cdXYxz3fOA3wt3y3RFKeRl8bZBZCRL5ZBs7lLBYPbknrtQdm13RmmchoaYl7sYHV0PyPlxUaVl0FTWhNIOpd5uiJbTJ0pCuXSR6GDIPbWEVuEacFNk0MexAAaDH58b4mcCbEaIE4XNIf221HVlRGYvhuds')


def post_insights_object(video_id, brand_name):
    end_date = datetime.datetime.today().strftime('%Y-%m-%d')
    graph = facebook_graph_object()
    insights = graph.request("319863888091100_" + str(video_id) + "/insights/")
    filepath = 'social_handles_data/' + brand_name + '/' + end_date +'_fb_insights.json'
    if not os.path.isfile(filepath):
        FileUtil.writeJson(filepath, {video_id: {"insights": insights, "meta_info": post_meta_info(video_id)}})
    else:
        data = FileUtil.readJson(filepath)
        if not (video_id in data.keys()):
            data[video_id] = {"insights": insights, "meta_info": post_meta_info(video_id)}
            FileUtil.writeJson(filepath, data)
    return insights

def post_meta_info(video_id):
    end_date = datetime.datetime.today().strftime('%Y-%m-%d')
    meta = {}
    print video_id, ""
    graph = facebook_graph_object()
    meta_info = graph.request("319863888091100_" + str(video_id) + "/")
    meta['video_title'] = meta_info['name']
    meta['created_date'] = meta_info['created_time']
    return meta

def get_insights(video_ids, brand_name):
    end_date = datetime.datetime.today().strftime('%Y-%m-%d')
    # video_ids = video_ids.split(',')
    for video_id in video_ids:
        post_insights_object(video_id, brand_name)

get_insights([u'887008244709992', u'877527895658027', u'934381439972672', u'874689175941899', u'914150505329099', u'878133152264168', u'914829691927847', u'945959322148217', u'940565752687574', u'924936864250463', '851685721575578', '871392976271519'], 'maybelline')
