import requests
import json
import csv
import facebook
import datetime


google_token = "Bearer ya29.kAK_5IQK061-wsBhUCYnbQ7JWXGpTXybCKlMMijlje2GoHRwwPEd4XL1-DBB9M9Ctjel"


video_ids = [
    {
        'fb': 863863537024463, 
        'yt': 'kxB-fIFTcG0'
    },
    {
        'fb': 864289866981830,
        'yt': 'kl_KhEJslN4'
    },
    {
        'fb': 863813073696176,  
        'yt': 'dv-LHg9X4-0'
    },
    {
        'fb': 843279482416202,
        'yt': '77VY8q2m0gk'
    },
    {
        'fb': 829381850472632,
        'yt': 'sTlPQLXbX0g'
    },
    {
        'fb': 786952974715520,
        'yt': 'yOcJUJgEsIg'
    },
    {
        'fb': 755004151243736,
        'yt': 'ZMkDQGGPjDo'
    },
    {
        'fb': 899305756813574,
        'yt': 'mn8yeT6Y-tQ'
    },
    {
        'fb': 896394667104683,
        'yt': '5qwgEoy4GoQ'
    },
    {
        'fb': 896632997080850,
        'yt': 'LS-KIUdobXc'
    },
    {
        'fb': 772150292862455,
        'yt': 'lxrVZInm0vI'
    },
    {
        'fb': 932669140143902,
        'yt': 'pFrUnz-NO7A'
    }
]

def get_youtube_video_ids():
    youtube_video_ids = []
    for each_dict in video_ids:
        youtube_video_ids.append(each_dict['yt'])
    return youtube_video_ids

def get_facebook_video_ids():
    facebook_video_ids = []
    for each_dict in video_ids:
        facebook_video_ids.append(each_dict['fb'])
    return facebook_video_ids

def get_youtube_title(title_info, video_id):
    for i in title_info:
        if i['id'] == video_id:
            title = i['title']
    return title


def post_insights_object(video_id):
    graph = facebook.GraphAPI(access_token='CAAGYi3qeYAIBAJTGZC5QdgWYaKQ71JvOICcYfKIeAXn8vKA1ZA2S2WnXoOZCC49llalYnMrwELeOTKF1UIgoDXBa2OjXz9PutEfLqN5g8wqxUBppvfkwWtluJkE2FQYYbbZBq1zW8598QmxYvJEv8Dqt6ZBviO3ZBX0jb6L8Fq9kzIIRTYHNZBvb2jCdXroBDMZD')
    insights = graph.request("319863888091100_" + str(video_id) + "/insights/")
    return json.dumps(insights)


def fetch_data():
    """
    Fetch views, likes, comments and shares for YouTube and Facebook videos
    :Input video ids should be given in following format.
    [
        {
            'fb': 932669140143902,
            'yt': 'pFrUnz-NO7A'
        },
    ]
    """
    start_date = '2011-01-01'
    end_date = datetime.datetime.today().strftime('%Y-%m-%d')
    youtube_video_ids = get_youtube_video_ids()
    facebook_video_ids = get_facebook_video_ids()
    final = []


    res = requests.get('https://www.googleapis.com/youtube/analytics/v1/reports?ids=channel%3D%3DUCXyq6UjvT4dWjMOOiKuBncA&start-date=' 
    + start_date +'&end-date=' + end_date + '&metrics=views%2Clikes%2Ccomments&filters=video%3D%3D' + ",".join(youtube_video_ids) + '&key={AIzaSyDT2HJjNdzVRVbxZKWh4PN_AuCxWeqVPsE}&dimensions=video', headers={'Authorization': google_token})
    youtubedata = res.json()

    snippet_data = requests.get('https://www.googleapis.com/youtube/v3/videos?part=snippet&id='+ ",".join(youtube_video_ids) +'&key={AIzaSyDT2HJjNdzVRVbxZKWh4PN_AuCxWeqVPsE}', headers={'Authorization': google_token})
    snippet = snippet_data.json()['items']
    title_info = []
    for i in snippet:
        kk = {}
        kk['id'] = i['id']
        kk['title'] = i['snippet']['title']
        title_info.append(kk)

    graph = facebook.GraphAPI(access_token='CAAGYi3qeYAIBAJTGZC5QdgWYaKQ71JvOICcYfKIeAXn8vKA1ZA2S2WnXoOZCC49llalYnMrwELeOTKF1UIgoDXBa2OjXz9PutEfLqN5g8wqxUBppvfkwWtluJkE2FQYYbbZBq1zW8598QmxYvJEv8Dqt6ZBviO3ZBX0jb6L8Fq9kzIIRTYHNZBvb2jCdXroBDMZD')
    all_fb = []
    for video_id in facebook_video_ids:
        insights = graph.request("319863888091100_" + str(video_id) + "/insights/")
        fb_title = graph.request("319863888091100_" + str(video_id) + "/")['name']
        post_video_views = insights['data'][25]['values'][0]['value']
        post_video_stories = insights['data'][57]['values'][0]['value']
        all_fb.append([video_id, post_video_views, post_video_stories['like'], post_video_stories['comment'], post_video_stories['share'], fb_title])
   
    youtube_grand_likes = []
    youtube_grand_views = []
    youtube_grand_comments = []
    facebook_grand_likes = []
    facebook_grand_views = []
    facebook_grand_comments = []
    facebook_grand_shares = []
    sum_total_views = []
    sum_total_likes = []
    sum_total_comments = []
    i = 0

    all_yb = []
    for video_id in video_ids:
        for yt_data in youtubedata['rows']:
            if video_id['yt'] == yt_data[0]:
                all_yb.append(yt_data)

    youtubedata["rows"] = all_yb

    while i < len(video_ids):
        each_video = {}
        each_video['facebook'] = {'video_id': all_fb[i][0], 'views':all_fb[i][1], 'likes':all_fb[i][2], 'comments': all_fb[i][3], 'shares': all_fb[i][4], 'video_title': all_fb[i][5]}

        each_video['youtube'] = {'video_id': youtubedata['rows'][i][0], 'views': youtubedata['rows'][i][1], 'likes': youtubedata['rows'][i][2], 'comments': youtubedata['rows'][i][3], 'video_title': get_youtube_title(title_info, youtubedata['rows'][i][0])}
        each_video['fb_yt'] = {'total_views': all_fb[i][1] + youtubedata['rows'][i][1], 'total_likes': all_fb[i][2] + youtubedata['rows'][i][2], 'total_comments': all_fb[i][3] + youtubedata['rows'][i][3]}
        final.append(each_video)
        youtube_grand_likes.append(youtubedata['rows'][i][2])
        youtube_grand_views.append(youtubedata['rows'][i][1])
        youtube_grand_comments.append(youtubedata['rows'][i][3])

        facebook_grand_likes.append(all_fb[i][2])

        facebook_grand_views.append(all_fb[i][1])
        facebook_grand_comments.append(all_fb[i][3])
        facebook_grand_shares.append(all_fb[i][4])

        sum_total_views.append(all_fb[i][1] + youtubedata['rows'][i][1])
        sum_total_likes.append(all_fb[i][2] + youtubedata['rows'][i][2])
        sum_total_comments.append(all_fb[i][3] + youtubedata['rows'][i][3])

        i = i + 1
    final.append(sum(facebook_grand_views))
    final.append(sum(youtube_grand_views))
    final.append(sum(sum_total_views))
    final.append(sum(facebook_grand_likes))
    final.append(sum(youtube_grand_likes))
    final.append(sum(sum_total_likes))
    final.append(sum(facebook_grand_comments))
    final.append(sum(youtube_grand_comments))
    final.append(sum(sum_total_comments))
    final.append(sum(facebook_grand_shares))
    return json.dumps(final)


def fetch_data_to_csv():
    """
    Fetch views, likes, comments and shares for YouTube and Facebook videos
    :Input video ids should be given in following format.
    : Generates CSV file with story values
    [
        {
            'fb': 932669140143902,
            'yt': 'pFrUnz-NO7A'
        },
    ]
    """
    start_date = '2016-01-01'
    end_date = datetime.datetime.today().strftime('%Y-%m-%d')
    youtube_video_ids = get_youtube_video_ids()
    facebook_video_ids = get_facebook_video_ids()

    res = requests.get('https://www.googleapis.com/youtube/analytics/v1/reports?ids=channel%3D%3DUCXyq6UjvT4dWjMOOiKuBncA&start-date=' 
    + start_date +'&end-date=' + end_date + '&metrics=views%2Clikes%2Ccomments&filters=video%3D%3D' + ",".join(youtube_video_ids) + '&key={AIzaSyDT2HJjNdzVRVbxZKWh4PN_AuCxWeqVPsE}&dimensions=video', headers={'Authorization': 'Bearer ya29.iwLAG83vcR1dyRSidaTAt8fEhD90YjnD0aQ5WzxOZmJgmGLwQuLvvkIFPV-sFhvutFDy'})
    youtubedata = res.json()
    graph = facebook.GraphAPI(access_token='CAAGYi3qeYAIBAJTGZC5QdgWYaKQ71JvOICcYfKIeAXn8vKA1ZA2S2WnXoOZCC49llalYnMrwELeOTKF1UIgoDXBa2OjXz9PutEfLqN5g8wqxUBppvfkwWtluJkE2FQYYbbZBq1zW8598QmxYvJEv8Dqt6ZBviO3ZBX0jb6L8Fq9kzIIRTYHNZBvb2jCdXroBDMZD')

    all_fb = []
    for video_id in facebook_video_ids:
        insights = graph.request("319863888091100_" + str(video_id) + "/insights/")
        post_video_views = insights['data'][25]['values'][0]['value']
        post_video_stories = insights['data'][57]['values'][0]['value']
        all_fb.append([video_id, post_video_views, post_video_stories['like'], post_video_stories['comment'], post_video_stories['share']])
    with open('fb_yt_stats.csv', 'a') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerow([])
        a.writerow(['Facebook Id','Facebook Views','Facebook Likes','Facebook Comments','Facebook Shares', 'Youtube Id', 'Youtube Views', 'Youtube Likes', 'Youtbe Comments'])
        for i in xrange(0, len(video_ids), 1):
            data = [
                [all_fb[i][0], all_fb[i][1], all_fb[i][2], all_fb[i][3], all_fb[i][4], youtubedata['rows'][i][0], youtubedata['rows'][i][1], youtubedata['rows'][i][2], youtubedata['rows'][i][3]]
            ]
            a.writerows(data)


if __name__ == "__main__":
    print fetch_data()
