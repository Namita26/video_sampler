import requests
import json
import facebook
import datetime
import os
from social_handles_data.utils.file_util import FileUtil


start_date = '2011-01-01'
end_date = datetime.datetime.today().strftime('%Y-%m-%d')


def get_youtube_video_ids(video_ids):
    youtube_video_ids = []
    for each_dict in video_ids:
        youtube_video_ids.append(each_dict['yt'])
    return youtube_video_ids

def refresh_access_token():
    refresh_token = "1/fMFAKHb_gsyWpG10RcpatvD8iMQvYug97dDuUEYYwZlIgOrJDtdun6zK6XiATCKT"
    payload = {
        'client_id': '816284744569-hblbg79baprfv7472kopc7q0ql53bn9b.apps.googleusercontent.com',
        'client_secret': 'J75434FzIp5RY87K-IVYkGaF',
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    refreshed_access_token = requests.post("https://accounts.google.com/o/oauth2/token", data=payload).json()['access_token']
    return refreshed_access_token

def post_insights_object(video_id):
    """
    Youtube insights
    """
    google_token = "Bearer ya29.kQIk-bNU4v5AaMwv-cNLLvhtZpSKMs-U_Xr75EwI_oauqqzd20monrJxCVYH9jBicRvX"
    insights = requests.get(
        'https://www.googleapis.com/youtube/analytics/v1/reports?ids=channel%3D%3DUCXyq6UjvT4dWjMOOiKuBncA&start-date=' + start_date +'&end-date=' + end_date + '&metrics=views%2Clikes%2Ccomments&filters=video%3D%3D' + video_id + '&key={AIzaSyDT2HJjNdzVRVbxZKWh4PN_AuCxWeqVPsE}&dimensions=video', headers={'Authorization': google_token}
    )
    if not ('rows' in insights.json().keys()):
        google_token = refresh_access_token()
        insights = requests.get(
            'https://www.googleapis.com/youtube/analytics/v1/reports?ids=channel%3D%3DUCXyq6UjvT4dWjMOOiKuBncA&start-date='+ start_date +'&end-date=' + end_date + '&metrics=views%2Clikes%2Ccomments&filters=video%3D%3D' + video_id + '&key={AIzaSyDT2HJjNdzVRVbxZKWh4PN_AuCxWeqVPsE}&dimensions=video', headers={'Authorization': 'Bearer '+google_token}
        )
    filepath = 'social_handles_data/'+ end_date +'_yt_insights.json'
    if not os.path.isfile(filepath):
        FileUtil.writeJson(filepath, {video_id: {"insights": insights.json()['rows'], "video_title":post_meta_info(video_id)}})
    else:
        data = FileUtil.readJson(filepath)
        if not (video_id in data.keys()):
            data[video_id] = {"insights": insights.json()['rows'], "video_title":post_meta_info(video_id)}
            FileUtil.writeJson(filepath, data)

    return insights

def post_meta_info(video_id):
    meta_info = requests.get('https://www.googleapis.com/youtube/v3/videos?part=snippet&id='+ video_id +'&key=AIzaSyCwMECGvrwK-WNC3zaHWEpOwPtCtRgT11I')
    return meta_info.json()['items'][0]['snippet']['title']


def make_analytics_api_request(youtube_video_ids, google_token):
    response = requests.get(
        'https://www.googleapis.com/youtube/analytics/v1/reports?ids=channel%3D%3DUCXyq6UjvT4dWjMOOiKuBncA&start-date=' + start_date +'&end-date=' + end_date + '&metrics=views%2Clikes%2Ccomments&filters=video%3D%3D' + youtube_video_ids + '&key={AIzaSyDT2HJjNdzVRVbxZKWh4PN_AuCxWeqVPsE}&dimensions=video', headers={'Authorization': "Bearer " + google_token}
    )
    return response


def make_data_api_request(youtube_video_ids):

    response = requests.get('https://www.googleapis.com/youtube/v3/videos?part=snippet&id='+youtube_video_ids+'&key=AIzaSyCwMECGvrwK-WNC3zaHWEpOwPtCtRgT11I')
    return response

def post_insights_object_combined(video_ids):
    youtube_video_ids = video_ids
    google_token = "Bearer ya29.kQIk-bNU4v5AaMwv-cNLLvhtZpSKMs-U_Xr75EwI_oauqqzd20monrJxCVYH9jBicRvX"

    insights = make_analytics_api_request(youtube_video_ids, google_token)

    if not ('rows' in insights.json().keys()):
        google_token = refresh_access_token()
        insights = make_analytics_api_request(youtube_video_ids, google_token)

    snippet_data = make_data_api_request(youtube_video_ids)

    youtubedata = insights.json()
    snippet = snippet_data.json()['items']
    title_info = []
    for title in snippet:
        titles = {}
        titles['id'] = title['id']
        titles['title'] = title['snippet']['title']
        title_info.append(titles)


    all_yb = []
    for video_id in video_ids.split(","):
        for yt_data in youtubedata['rows']:
            if video_id == yt_data[0]:
                all_yb.append(yt_data)
    with open("social_handles_data/"+ end_date  +"yt_stats.json", "w") as f:
        json.dump({"youtube": all_yb, 'title_info': title_info}, f, indent=4)
    return [all_yb, title_info]


def get_insights(ids):
    post_insights_object_combined(ids)


if __name__ == "__main__":
    get_insights('kxB-fIFTcG0,kl_KhEJslN4,dv-LHg9X4-0,77VY8q2m0gk,sTlPQLXbX0g,yOcJUJgEsIg,ZMkDQGGPjDo,mn8yeT6Y-tQ,5qwgEoy4GoQ,LS-KIUdobXc,lxrVZInm0vI,pFrUnz-NO7A')
