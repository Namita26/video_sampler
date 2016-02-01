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


def fetch_data():
    """
    Fetch facebook retention values for video that we upload!
    :param video_id: facebook video id for glamrs video.
    """
    graph = facebook.GraphAPI(access_token='CAAGYi3qeYAIBAOaska4bnaApnDoRcZBd0XxV9WkDSzfVE8z9MTQKGR4BNZCJF3vc84SpSmhaeIwTXcVnIvGnWqu72reJHSRAvJmAZCHLpIyZCKssXCP5fgFLPxolgPGAZCZCBnGoyOEquPdjgpkEPU3vKBIvR1ODPd2yi3nx3TKI31WZBfrxrjRBhmC3aBJrQmbvXMMntlwuQZDZD', timeout=100)
    # access token have to be refreshed after specifies timeout parameter. Get it from https://developers.facebook.com/tools/explorer/
    y_values = graph.request("319863888091100_949859058424910/insights/post_video_retention_graph/lifetime")['data'][0]['values'][0]['value']
    output = []
    count = 0
    for y_value in y_values:
        output.append([count * 2.5, y_value])
        count = count + 1

    # return json.dumps({"x_values": x_values, "y_values":y_values})
    return json.dumps(output)


if __name__ == "__main__":
   print fetch_data()
