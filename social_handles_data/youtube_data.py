import requests
import json


def fetch_data(id):
    """
    Fetch youtube retention values for video that we upload!
    :param video_id: facebook video id for glamrs video.
    """
    res = requests.get('https://www.googleapis.com/youtube/analytics/v1/reports?ids=channel%3D%3DUCXyq6UjvT4dWjMOOiKuBncA&start-date=2016-01-01&end-date=2016-01-23&metrics=audienceWatchRatio&dimensions=elapsedVideoTimeRatio&filters=video%3D%3D' + id + '&key={AIzaSyDT2HJjNdzVRVbxZKWh4PN_AuCxWeqVPsE}', headers={'Authorization': 'Bearer ya29.fAJ4MiDT3fgqPDvgeVPlw763E5od5mL53wEgzzfhi2bz97Xy4WhkJbwmK69x0qJlNZLy'})
    youtubedata = res.json()
    output = []
    for arr in youtubedata["rows"]:
        output.append(arr[1])
    return json.dumps(output)

if __name__ == "__main__":
    print fetch_data('UYpoq0-Lamw')
