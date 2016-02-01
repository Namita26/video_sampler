import requests
import json


def fetch_data():
    """
    Fetch youtube retention values for video that we upload!
    :param video_id: facebook video id for glamrs video.
    """
    res = requests.get('https://www.googleapis.com/youtube/analytics/v1/reports?ids=channel%3D%3DUCXyq6UjvT4dWjMOOiKuBncA&start-date=2016-01-01&end-date=2016-01-23&metrics=audienceWatchRatio&dimensions=elapsedVideoTimeRatio&filters=video%3D%3DUYpoq0-Lamw&key={AIzaSyDT2HJjNdzVRVbxZKWh4PN_AuCxWeqVPsE}', headers={'Authorization': 'Bearer ya29.ewLFB0uPhLSOEjb2SSZF0mSYf-8qu9pcext8sAkWT3WP9kBG92Eqa54k7S6GOAzHEiEU'})
    youtubedata = res.json()
    output = []
    for arr in youtubedata['rows']:
        output.append([arr[0] * 100, arr[1]])
    return json.dumps(output)

if __name__ == "__main__":
    fetch_data()
