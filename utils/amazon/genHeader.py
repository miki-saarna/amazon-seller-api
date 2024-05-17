import requests
import json

import const as const

access_endpoint = "https://api.amazon.com/auth/o2/token"

access_params = {
    "grant_type": "refresh_token",
    "refresh_token": const.REFRESH_TOKEN,
    "client_id": const.LWA_APP_ID,
    "client_secret": const.CLIENT_SECRET,
}

def genHeader():
    res = requests.post(access_endpoint, params=access_params)
    data = json.loads(res.text)
    access_token = data["access_token"]

    headers = {
        'content-type': 'application/json',
        'x-amz-access-token': access_token
    }

    return headers


if __name__ == '__main__':
    genHeader()
