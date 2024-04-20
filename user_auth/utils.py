from django.contrib.auth import get_user_model
import requests, base64

from constant import Constants

def response_data(error, message, data=None):
    if data:
        return {"error": error, "data": data, "message": message}
    else:
        return {"error": error, "message": message}

def OauthGetToken(username, password):
    url = Constants.OAUTH_URL
    payload  = {
        "grant_type": Constants.GRANT_TYPE,
        "username": username,
        "password": password
    }
    credentials = f'{Constants.CLIENT_ID}:{Constants.CLIENT_SECRET}'
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encoded_credentials}'
    }
    response = requests.post(url, data= payload, headers= headers)
    return response, response.status_code
