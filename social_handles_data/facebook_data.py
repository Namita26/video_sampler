"""
@author: Namita Goyal
Date: 28 Jan, 2016

Fetch video information from facebook GraphAPI
"""

from __future__ import division
import facebook   # python client lib for facebook GraphAPI 
import json


def _generate_x_values():
    """
    Generates array of values from 0-40.
    """
    x_values = []
    for val in xrange(0, 41, 1):
        x_values.append(val*100/41)
    return x_values


def create_graph_object():
    """
    Creates Facebook GraphAAPI object and returns it.
    """
    graph = facebook.GraphAPI(access_token='CAAGYi3qeYAIBAJTGZC5QdgWYaKQ71JvOICcYfKIeAXn8vKA1ZA2S2WnXoOZCC49llalYnMrwELeOTKF1UIgoDXBa2OjXz9PutEfLqN5g8wqxUBppvfkwWtluJkE2FQYYbbZBq1zW8598QmxYvJEv8Dqt6ZBviO3ZBX0jb6L8Fq9kzIIRTYHNZBvb2jCdXroBDMZD')
    return graph


def get_video_ids():
    graph = create_graph_object()
    video_ids = []
    data_points = graph.request("319863888091100/posts/", {type:'video'})
    for each in data_points['data']:
        video_details = {}
        if each['type'] == 'video':
            video_details['video_id'] = each['id']
            video_details['video_title'] = each['message']
            # video_details[each['id']] = each['message']
            video_ids.append(video_details)
    return json.dumps(video_ids)
    

def fetch_data(id):
    """
    Fetch facebook retention values for video that we upload!
    :param video_id: facebook video id for glamrs video.
    """
    graph = facebook.GraphAPI(access_token='CAAGYi3qeYAIBAJTGZC5QdgWYaKQ71JvOICcYfKIeAXn8vKA1ZA2S2WnXoOZCC49llalYnMrwELeOTKF1UIgoDXBa2OjXz9PutEfLqN5g8wqxUBppvfkwWtluJkE2FQYYbbZBq1zW8598QmxYvJEv8Dqt6ZBviO3ZBX0jb6L8Fq9kzIIRTYHNZBvb2jCdXroBDMZD')

    # permanent access token
    sorted_values = []
    facebook_xy_values = graph.request(id + "/insights/post_video_retention_graph/lifetime")['data'][0]['values'][0]['value']
    if type(facebook_xy_values) == list:
        return json.dumps(facebook_xy_values)
    elif type(facebook_xy_values) == dict:
        for i in xrange(0, len(facebook_xy_values), 1):
            sorted_values.append(facebook_xy_values[str(i)])
        return json.dumps(sorted_values)


if __name__ == "__main__":
   fetch_data()
