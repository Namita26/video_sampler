import facebook
import requests
from social_handles_data.fbstories import get_only_facebook_stories

def get_graph_handle():
    return facebook.GraphAPI(access_token='CAAGYi3qeYAIBAOsFnZCg7SZACH9cdXYxz3fOA3wt3y3RFKeRl8bZBZCRL5ZBs7lLBYPbknrtQdm13RmmchoaYl7sYHV0PyPlxUaVl0FTWhNIOpd5uiJbTJ0pCuXSR6GDIPbWEVuEacFNk0MexAAaDH58b4mcCbEaIE4XNIf221HVlRGYvhuds')

def first_Call():

    videos = {
        "851685721575578" : ["lipstick-hacks-every-girl-needs-to-know", "http://glam.rs/1NuHYvx", "/post/6060"],
        "871392976271519" : ["7-genius-ways-to-use-a-compact-powder", "http://bit.ly/1ZPwISA", "/post/3466"]
    }

    since = 1439712000
    until = 1458135310
    timestamp = {"type": "video", "since": since, "until": until, "fields": "link", "limit":100}

    video_ids = {
        "851685721575578": ['319863888091100_851685721575578'],
        "871392976271519": ['319863888091100_871392976271519']
    }

    graph = get_graph_handle()

    initial = graph.request("319863888091100/posts/", timestamp)
    response = initial
    for i in response['data']:
        for video, links in videos.iteritems():
            for link in links:
                if link in i.get('link', ''):
                    video_ids[video].append(i['id'])

    next_request_url = response['paging']['next']

    while next_request_url:
        response = requests.get(next_request_url)
        data = response.json()
        if response.status_code != 200:
            break
        next_request_url = data.get('paging', {}).get('next', "")
        for i in data['data']:
            for video, links in videos.iteritems():
                for link in links:
                    if link in i.get('link', ""):
                        video_ids[video].append(i['id'])

    return video_ids


def get_combined_insights(video_id):

    print "\n---------\n"
    print "In get_total_impressions:", video_id
    print "\n---------\n"
    data = {'871392976271519': [u'319863888091100_934381439972672', u'319863888091100_934381439972672', u'319863888091100_914829691927847', u'319863888091100_914829691927847', u'319863888091100_914150505329099', u'319863888091100_887008244709992', u'319863888091100_878133152264168', u'319863888091100_877527895658027', u'319863888091100_874689175941899'], '851685721575578': [u'319863888091100_945959322148217', u'319863888091100_940565752687574', u'319863888091100_924936864250463']}
    
    ids = data.get(str(video_id), [])  
    fb_video_ids = list(set([id.split("_")[-1] for id in ids]))
    print fb_video_ids
    total_impressions = get_total_impressions(fb_video_ids)
    print total_impressions
    return total_impressions


def get_total_impressions(video_ids):
    total_impressions = 0
    graph = get_graph_handle()
    for video_id in video_ids:
        insights = graph.request("319863888091100_" + video_id + "/insights")
        total_impressions += insights['data'][5]['values'][0]['value']
    return total_impressions

def status(next_request_url):
    return requests.get(next_request_url)

if __name__ == "__main__":
    #x = first_Call()
    #print x
    #print len(x)
    print get_combined_insights("871392976271519")
