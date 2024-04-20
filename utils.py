from django.contrib.auth import get_user_model
import requests, base64, random, string

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

def generate_leadID(length=6):
    """Generate a random Lead_id of specified length."""

    lead_id = "ld_" + "".join(random.choices(string.digits, k=length))
    return lead_id


def generate_random_string(length=10):
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for _ in range(length))