from django.contrib.auth import get_user_model
import requests, base64, random, string

from constant import Constants
import boto3, os
from dotenv import load_dotenv

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

import json

load_dotenv()

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
    print("client ID : ", os.environ.get("CLIENT_ID"), ", Client secret: ",os.environ.get("CLIENT_SECRET") )
    credentials = f'{os.environ.get("CLIENT_ID")}:{os.environ.get("CLIENT_SECRET")}'
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encoded_credentials}'
    }
    response = requests.post(url, data= payload, headers= headers)
    return response, response.status_code

def make_s3_connection():
    try:
        ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
        SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
        s3_conn_obj = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
        return s3_conn_obj
    except:
        return None

def upload_file_to_s3_bucket(s3_conn, file, bucket_name, file_key):
    try:
        s3_conn.put_object(Body=file.read(), Bucket=bucket_name, Key=file_key)
        file_url = f"s3://{bucket_name}/{file_key}"
        return str(file_url)
    except Exception as e:
        return False

def generate_leadID(length=6):
    """Generate a random Lead_id of specified length."""

    lead_id = "ld_" + "".join(random.choices(string.digits, k=length))
    return lead_id

def generate_applicationID(length=8):
    """Generate a random applicante_id of specified length."""

    applicante_id = "app_" + "".join(random.choices(string.digits, k=length))
    return applicante_id

def generate_customerID(length=8):
    """Generate a random customer_id of specified length."""

    customer_id = "cif_" + "".join(random.choices(string.digits, k=length))
    return customer_id


def generate_PaymentID(length=8):
    """Generate a random payment of specified length."""

    Payment_id = "pmt_" + "".join(random.choices(string.digits, k=length))
    return Payment_id

def generate_locanID(length=8):
    """Generate a random payment of specified length."""

    loan_id = "pmt_" + "".join(random.choices(string.digits, k=length))
    return loan_id

def generate_random_string(length=10):
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for _ in range(length))

def calculate_sha256_string(input_string):
    sha256 = hashes.Hash(hashes.SHA256(), backend=default_backend())
    sha256.update(input_string.encode('utf-8'))
    return sha256.finalize().hex()

def base64_encode(input_dict):
    json_data = json.dumps(input_dict)
    data_bytes = json_data.encode('utf-8')
    return base64.b64encode(data_bytes).decode('utf-8')
