import requests
import json
from utils.yt import post_meta_info, refresh_access_token


def fetch_data(id):
    """
    Fetch youtube retention values for video that we upload!
    :param video_id: facebook video id for glamrs video.
    """
    res = requests.get('https://www.googleapis.com/youtube/analytics/v1/reports?ids=channel%3D%3DUCXyq6UjvT4dWjMOOiKuBncA&start-date=2016-01-01&end-date=2016-01-23&metrics=audienceWatchRatio&dimensions=elapsedVideoTimeRatio&filters=video%3D%3D' + id + '&key={AIzaSyDT2HJjNdzVRVbxZKWh4PN_AuCxWeqVPsE}', headers={'Authorization': 'Bearer ya29.qALms2RdInTJ9uJ2H179wtAOFtqGCtIMPf5H57kIfAfVlJhfiOGkqqYZ1sQw'})

    if not ('rows' in res.json().keys()):
        google_token = refresh_access_token()
        res = requests.get('https://www.googleapis.com/youtube/analytics/v1/reports?ids=channel%3D%3DUCXyq6UjvT4dWjMOOiKuBncA&start-date=2016-01-01&end-date=2016-01-23&metrics=audienceWatchRatio&dimensions=elapsedVideoTimeRatio&filters=video%3D%3D' + id + '&key={AIzaSyDT2HJjNdzVRVbxZKWh4PN_AuCxWeqVPsE}', headers={'Authorization': 'Bearer ' + google_token})


    youtubedata = res.json()
    output = []
    for arr in youtubedata["rows"]:
        output.append(arr[1])
    return json.dumps({"yt_retention_values": output, "yt_video_title": post_meta_info(id)})

def get_video_title(video_id):
    return post_meta_info(video_id)

if __name__ == "__main__":
    print fetch_data('UYpoq0-Lamw')
    # print post_meta_info('UYpoq0-Lamw')
