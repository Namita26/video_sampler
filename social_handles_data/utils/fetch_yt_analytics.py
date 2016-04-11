import requests


def refresh_access_token():

    payload = {
        "refresh_token": "1/eP7zTuVNkjTELesHQknC5Rb8J5O4AVtU_XfWrZXDWhEMEudVrK5jSpoR30zcRFq6",
        "client_secret": "J75434FzIp5RY87K-IVYkGaF",
        "client_id": "816284744569-hblbg79baprfv7472kopc7q0ql53bn9b.apps.googleusercontent.com",
        "grant_type": "refresh_token"
    }
    refreshed_access_token = requests.post("https://accounts.google.com/o/oauth2/token", data=payload).json()
    return refreshed_access_token


def glamrs_youtube_views(video_id):
    vmap = {
        "ubePCsGXcUE": "7-genius-ways-to-use-a-compact-powder",
        "-7MV-cspVXM": "lipstick-hacks-every-girl-needs-to-know"
    }
    video = vmap[video_id]
    res = requests.get("https://www.googleapis.com/analytics/v3/data/ga?ids=ga%3A67237418&start-date=2015-01-01&end-date=today&metrics=ga%3Apageviews&dimensions=ga%3ApagePath&filters=ga%3ApagePath%3D%40" + video, headers={"Authorization": "Bearer ya29..wQJX0Y5Is58YqCk4BIlVIytMAP6cziOCyCOaIzafichTwVvbqd2NJ3DYAwfhgrvGLA"})
    return sum([int(row[1]) for row in res.json()['rows']])

if __name__ == "__main__":
    print refresh_access_token()
