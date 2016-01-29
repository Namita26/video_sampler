"""
@author: Namita Goyal
Date: 28 Jan, 2016

Fetch video information from facebook GraphAPI
"""

import facebook   # python client lib for facebook GraphAPI 
import json


def _generate_x_values():
    """
    Generates array of values from 0-40.
    """
    x_values = []
    for val in xrange(0, 40, 1):
        x_values.append(val)
    return x_values


def fetch_data():
    """
    Fetch facebook retention values for video that we upload!
    :param video_id: facebook video id for glamrs video.

    Return Values: Json object containing  [x_values, y_values].  
    :x_values: X Axis values for Line Graph. This would be constant. 
    :y_values: Y Axis values for Line Graph.
    """
    print "In fetch data facebook--------------------------------\n\n"
    print facebook
    graph = facebook.GraphAPI(access_token='CAAGYi3qeYAIBAOZCTZAFDYaRd7ZAy6wchz3q7jPuoKJbswp8PGMbvM2VQICZAlOGjPYM3SpttPqHDaXvQ5CTQBKYaxJtAALYKEzoayNJ5Q9vhrV4UOv0C60qVe6NnxRJZBYxZCPFI2wWvwEj6jqcdeXQ9V87h3Cp7jxi4qZCbiWfRxLljPBnCJZCw6ysKZCYZBf2cZD', timeout=100)
    # access token have to be refreshed after specifies timeout parameter. Get it from https://developers.facebook.com/tools/explorer/
    y_values = graph.request("319863888091100_949859058424910/insights/post_video_retention_graph/lifetime")['data'][0]['values'][0]['value']
    '''
    final = []
    for val in xrange(0, 40, 2):
        final.append(y_values[val])
    '''
    x_values = _generate_x_values()
    return json.dumps({"x_values": x_values, "y_values":y_values})

if __name__ == "__main__":
   print fetch_data()
