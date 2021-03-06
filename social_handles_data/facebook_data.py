"""
@author: Namita Goyal
Date: 28 Jan, 2016

Fetch video information from facebook GraphAPI
"""

from __future__ import division
import facebook   # python client lib for facebook GraphAPI 
import json
import collections
import operator
from utils.fb import post_meta_info


def get_video_title(video_id):
    graph = create_graph_object()
    result = graph.request(video_id + "/", {type:'video'})
    return result['name']

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
    graph = facebook.GraphAPI(access_token='CAAGYi3qeYAIBAOsFnZCg7SZACH9cdXYxz3fOA3wt3y3RFKeRl8bZBZCRL5ZBs7lLBYPbknrtQdm13RmmchoaYl7sYHV0PyPlxUaVl0FTWhNIOpd5uiJbTJ0pCuXSR6GDIPbWEVuEacFNk0MexAAaDH58b4mcCbEaIE4XNIf221HVlRGYvhuds')
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
    graph = create_graph_object()

    # permanent access token
    sorted_values = []
    facebook_xy_values = graph.request(id + "/insights/post_video_retention_graph/lifetime")['data'][0]['values'][0]['value']
    title = get_video_title(id)
    if type(facebook_xy_values) == list:
        return json.dumps({"fb_retention_values": facebook_xy_values, "fb_video_title": title})
    elif type(facebook_xy_values) == dict:
        for i in xrange(0, len(facebook_xy_values), 1):
            sorted_values.append(facebook_xy_values[str(i)])
        return json.dumps({"fb_video_title": title, "fb_retention_values": sorted_values})


def get_fans_timeline_data(since, until):
    graph = create_graph_object()
    timestamp = {"since": since, "until": until}
    print timestamp
    insights = graph.request("319863888091100/insights/", timestamp)
    dates_on_x_axis = _extract_dates(insights['data'][0]['values'])
    likes = new_likes(insights['data'][0]['values'])
    dislikes = new_dislikes(insights['data'][3]['values'])
    paid_impressions = new_paid_fans(insights['data'][2]['values'])
    organic_fans = new_organic_fans(insights['data'][2]['values'])
    
    total_gain = total_fans_gained(since, until)
    total_loss = total_fans_lost(since, until)

    return json.dumps(
        {
            "x_axis_dates": dates_on_x_axis,
            "likes": likes,
            "dislikes": dislikes,
            "paid_fans": paid_impressions,
            "organic_fans": organic_fans,
            "fans_lost": total_loss[0],
            "fans_lost_percentage": total_loss[1],
            "fans_gained": total_gain[0],
            "fans_gained_percentage": total_gain[1],
            "fans_gain_to_loss_ratio": fans_gained / fans_lost
        },
        indent=4
    )


def total_fans_gained(since, until):
    graph = create_graph_object()
    since = int(since)
    until = int(until)
    print since, until, type(since), type(until), "\n---"
    timestamp = {"since": since, "until": until}
    insights = graph.request("319863888091100/insights/", timestamp)
    likes = new_likes(insights['data'][0]['values'])
    pos_gain = sum(likes)

    new_since = since - (until - since)
    new_until = since
    timestamp = {"since": new_since, "until": new_until}
    insights = graph.request("319863888091100/insights/", timestamp)
    likes = new_likes(insights['data'][0]['values'])
    pre_gain = sum(likes)
    
    return [pos_gain, abs(pos_gain - pre_gain) *100 / pre_gain]

def total_fans_lost(since, until):
    graph = create_graph_object()
    timestamp = {"since": since, "until": until}
    insights = graph.request("319863888091100/insights/", timestamp)
    unlikes = new_likes(insights['data'][3]['values'])
    pos_loss = sum(unlikes)

    new_since = since - (until - since)
    new_until = since
    timestamp = {"since": new_since, "until": new_until}
    insights = graph.request("319863888091100/insights/", timestamp)
    unlikes = new_likes(insights['data'][3]['values'])
    pre_loss = sum(unlikes)

    return [pos_loss, abs(pos_loss- pre_loss) *100 / pre_loss]

def total_fans(since, until):
    graph = create_graph_object()
    timestamp = {"since": since, "until": until}
    insights = graph.request("319863888091100/insights/", timestamp)
    return insights['data'][171]['values'][7]['value']    


def new_likes(raw_values):
    likes = []
    for each in raw_values:
        likes.append(each['value'])
    return likes


def new_dislikes(raw_values):
    dislikes = []
    for each in raw_values:
        dislikes.append(each['value'])
    return dislikes


def new_paid_fans(raw_values):
    paid_fans = []
    for each in raw_values:
        paid_fans.append(each['value']['paid'])
    return paid_fans


def new_organic_fans(raw_values):
    organic_fans = []
    for each in raw_values:
        organic_fans.append(each['value']['unpaid'])
    return organic_fans


def get_gain_loss_fans_data(since, until):
    graph = create_graph_object()
    timestamp = {"since": since, "until": until}
    insights = graph.request("319863888091100/insights/", timestamp)
    dates_on_x_axis = _extract_dates(insights['data'][0]['values'])
    gains = new_likes(insights['data'][0]['values'])
    losses = new_dislikes(insights['data'][3]['values'])
    gain_to_loss = gain_loss(gains, losses)
    return json.dumps(
        {
            "x_axis_dates": dates_on_x_axis,
            "Gain To Loss Ratios": gain_to_loss
        }
    )


def gain_loss(gains, losses):
    from operator import truediv
    ratios = map(truediv, gains, losses)
    return ratios

def _extract_dates(raw_values):
    extracted_timestamp_dates = []
    for each in raw_values:
        raw_date = each['end_time'].split('T')
        extracted_timestamp_dates.append(raw_date[0])
    return extracted_timestamp_dates


def page_like_by_sources(since, until):
    graph = create_graph_object()
    timestamp = {"since": since, "until": until}
    insights = graph.request("319863888091100/insights/", timestamp)

    all_sources_data = insights['data'][148]['values']
    # desired_sources = ['feed_story', 'mobile_ads', 'page_profile', 'feed_pyml', 'sponsored_story', 'ads', 'mobile', 'api']
    return json.dumps(
        {
            'feed_story': get_sources_data(all_sources_data, 'feed_story'),
            'mobile_ads': get_sources_data(all_sources_data, 'mobile_ads'),
            'page_profile': get_sources_data(all_sources_data, 'page_profile'), 
            'feed_pyml': get_sources_data(all_sources_data, 'feed_pyml'),
            'sponsored_story': get_sources_data(all_sources_data, 'sponsored_story'),
            'ads': get_sources_data(all_sources_data, 'ads'),
            'mobile': get_sources_data(all_sources_data, 'mobile'), 
            'api': get_sources_data(all_sources_data, 'api')
        }
    )

def get_sources_data(all_sources_data, source):
    data_values = []
    for i in all_sources_data:
        data_values.append(i['value'][source])
    return sum(data_values)


def page_gender_and_age_group_fans(since, until):
    male_dict = {}
    female_dict = {}
    graph = create_graph_object()
    timestamp = {"since": since, "until": until}
    insights = graph.request("319863888091100/insights/", timestamp)
    overall_data = insights['data'][177]['values'][6]['value']
    for key, val in overall_data.iteritems():
        if 'F' in key:
            female_dict[key] = val
        elif 'M' in key:
            male_dict[key] = val
    return json.dumps(
        {
            "males": collections.OrderedDict(sorted(male_dict.items())).values(),
            "females": collections.OrderedDict(sorted(female_dict.items())).values()
        }
    )

def page_country_wise_fans(since, until):
    graph = create_graph_object()
    timestamp = {"since": since, "until": until}
    insights = graph.request("319863888091100/insights/", timestamp)
    country_data = insights['data'][174]['values'][6]['value']
    
    sorted_countries = sorted(country_data.items(), key=operator.itemgetter(1))
    ordered_countries_names = []
    ordered_countries_fans = []

    for i in reversed(sorted_countries):
        ordered_countries_names.append(i[0])
        ordered_countries_fans.append(i[1])

    return json.dumps(
        {
            "countries": ordered_countries_names,
            "fans": ordered_countries_fans
        }
    )

def page_city_wise_fans(since, until):
    graph = create_graph_object()
    timestamp = {"since": since, "until": until}
    insights = graph.request("319863888091100/insights/", timestamp)
    cities = insights['data'][173]['values'][6]['value']
    
    sorted_cities = sorted(cities.items(), key=operator.itemgetter(1))
    ordered_city_names = []
    ordered_city_fans = []

    for i in reversed(sorted_cities):
        ordered_city_names.append(i[0].split(',')[0])
        ordered_city_fans.append(i[1])

    return json.dumps(
        {
            "cities": ordered_city_names,
            "fans": ordered_city_fans
        }
    )

    
def page_reach(since, until):
    graph = create_graph_object()
    timestamp = {"since": since, "until": until}
    insights = graph.request("319863888091100/insights/", timestamp)
    dates_on_x_axis = _extract_dates(insights['data'][0]['values'])
    page_impressions_unique = new_page_impressions_unique(insights['data'][49]['values'])
    page_impressions_unique_organic = new_page_impressions_unique(insights['data'][61]['values'])
    paid_impressions_viral = new_page_impressions_unique(insights['data'][67]['values'])
    return json.dumps(
        {
            "x_axis_dates": dates_on_x_axis,
            "total_reach": page_impressions_unique,
            "total_organic_reach": page_impressions_unique_organic,
            "total_viral_reach": paid_impressions_viral,
        }
    )


def new_page_impressions_unique(raw_values):
    likes = []
    for each in raw_values:
        likes.append(each['value'])
    return likes


def page_impressions(since, until):
    graph = create_graph_object()
    timestamp = {"since": since, "until": until}
    insights = graph.request("319863888091100/insights/", timestamp)
    dates_on_x_axis = _extract_dates(insights['data'][0]['values'])
    impressions = new_page_impressions(insights['data'][52]['values'])
    paid_impressions = new_page_impressions(insights['data'][58]['values'])
    organic_impressions = new_page_impressions(insights['data'][64]['values'])
    viral_impressions = new_page_impressions(insights['data'][70]['values'])
    return json.dumps(
        {
            "x_axis_dates": dates_on_x_axis,
            "impressions": impressions,
            "organic": organic_impressions,
            "viral": viral_impressions,
            "paid_impressions": paid_impressions
        }
    )


def new_page_impressions(raw_values):
    likes = []
    for each in raw_values:
        likes.append(each['value'])
    return likes


def page_performance(since, until):
    graph = create_graph_object()
    timestamp = {"since": since, "until": until}
    insights = graph.request("319863888091100/insights/", timestamp)
    dates_on_x_axis = _extract_dates(insights['data'][0]['values'])
    impressions = new_page_performance(insights['data'][52]['values'])
    stories = new_page_performance(insights['data'][212]['values'])
    engagements = new_page_performance(insights['data'][195]['values'])
    unique_users = new_page_performance(insights['data'][138]['values'])
    return json.dumps(
        {
            "x_axis_dates": dates_on_x_axis,
            "impressions": impressions,
            "stories": stories,
            "engagements": engagements,
            "unique_users": unique_users
        }
    )


def new_page_performance(raw_values):
    likes = []
    for each in raw_values:
        likes.append(each['value'])
    return likes


def page_negative_feedback(since, until):
    graph = create_graph_object()
    timestamp = {"since": since, "until": until}
    insights = graph.request("319863888091100/insights/", timestamp)
    dates_on_x_axis = _extract_dates(insights['data'][0]['values'])
    page_unlikes = new_page_performance(insights['data'][3]['values'])
    post_page_unlike = post_page_unlikes(insights['data'][162]['values'])
    hide_posts = hide_clicks(insights['data'][162]['values'])
    hide_all_posts = hide_all_clicks(insights['data'][162]['values'])
    spam = report_spam(insights['data'][162]['values'])
    return json.dumps(
        {
            "x_axis_dates": dates_on_x_axis,
            "Page Unlikes": page_unlikes,
            "Post Page Unlikes": post_page_unlike,
            "Hide Posts": hide_posts,
            "Hide All": hide_all_posts,
            "Spam": spam
        }
    )


def hide_all_clicks(raw_values):
    hide_all_clicks = []
    for each in xrange(0, len(raw_values), 1):
        hide_all_clicks.append(raw_values[each]['value']['hide_all_clicks'])
    return hide_all_clicks


def hide_clicks(raw_values):
    hide_clicks = []
    for each in xrange(0, len(raw_values), 1):
        hide_clicks.append(raw_values[each]['value']['hide_clicks'])
    return hide_clicks


def report_spam(raw_values):
    spams = []
    for each in xrange(0, len(raw_values), 1):
        spams.append(raw_values[each]['value']['report_spam_clicks'])
    return spams


def post_page_unlikes(raw_values):
    post_page_unlikes = []
    for each in xrange(0, len(raw_values), 1):
        post_page_unlikes.append(raw_values[each]['value']['unlike_page_clicks'])
    return post_page_unlikes


def report_spam(raw_values):
    spams = []
    for each in xrange(0, len(raw_values), 1):
        spams.append(raw_values[each]['value']['report_spam_clicks'])
    return spams

def page_insights(since, until):
    graph = create_graph_object()
    timestamp = {"since": since, "until": until}
    insights = graph.request("319863888091100/insights/", timestamp)
    return json.dumps(
        {
            "insights": insights['data'] 
        }
    )


if __name__ == "__main__":
    # fetch_data()
    since = 1452672000
    until = 1453363200
    new_since = since - (until - since)
    new_until = since
    # print new_since, new_until
    # print get_fans_timeline_data(since, until)
    # print get_gain_loss_fans_data(1452758400, 1453363200)
    # print page_like_by_sources(1452758400, 1453363200)
    # print page_gender_and_age_group_fans(1452758400, 1453363200)
    # print page_country_wise_fans(1452758400, 1453363200)
    # print page_city_wise_fans(1452758400, 1453363200)
    # print page_reach(1452758400, 1453363200)
    # print page_impressions(1452758400, 1453363200)
    # print page_performance(1452758400, 1453363200)
    # print page_negative_feedback(1452758400, 1453363200)
    # print total_fans_gained(since, until)
    # print total_fans_lost(since, until)
    print get_video_title("319863888091100_871392976271519")
