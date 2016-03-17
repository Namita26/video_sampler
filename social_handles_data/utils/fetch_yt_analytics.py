import requests


def refresh_access_token():
    refresh_token = "1/eP7zTuVNkjTELesHQknC5Rb8J5O4AVtU_XfWrZXDWhEMEudVrK5jSpoR30zcRFq6"
    payload = {
        'client_id':  "816284744569-hblbg79baprfv7472kopc7q0ql53bn9b.apps.googleusercontent.com",
        'client_secret': 'J75434FzIp5RY87K-IVYkGaF',
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    refreshed_access_token = requests.post("https://accounts.google.com/o/oauth2/token", data=payload).json()
    return refreshed_access_token

if __name__ == "__main__":
    print refresh_access_token()
