import requests
import json


def fetch_data():
    res = requests.get('https://www.googleapis.com/youtube/analytics/v1/reports?ids=channel%3D%3DUCXyq6UjvT4dWjMOOiKuBncA&start-date=2016-01-01&end-date=2016-01-23&metrics=audienceWatchRatio&dimensions=elapsedVideoTimeRatio&filters=video%3D%3DUYpoq0-Lamw&key={AIzaSyDT2HJjNdzVRVbxZKWh4PN_AuCxWeqVPsE}', headers={'Authorization': 'Bearer ya29.eALPbVPMy-ujq2jwTvvtVwAEppRPCb8Whynaeo5W9MNzNqaSZxTqMsf3obq91_ciWDm3'})
    youtubedata = res.json()
    yt_y_values = []
    yt_x_values = []
    for arr in youtubedata['rows']:
        yt_y_values.append(arr[1])
        yt_x_values.append(arr[0])
    counter = 0
    """
    final = []
    for counter in xrange(0, 100, 5):
        final.append(yt_y_values[counter])
    """
    return json.dumps({"yt_y_values": yt_y_values, "yt_x_values": yt_x_values})

if __name__ == "__main__":
    print fetch_data()
