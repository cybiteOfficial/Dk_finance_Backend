from django.contrib.auth import get_user_model
import requests, base64, random, string
from constant import Constants

import logging
import boto3, os
from botocore.exceptions import ClientError
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
    url = os.environ.get('OAUTH_URL')
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
        REGION = os.environ.get('REGION')
        s3_conn_obj = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name = REGION)
        return s3_conn_obj
    except:
        return None

def upload_file_to_s3_bucket(s3_conn, file, bucket_name, file_key):
    try:
        s3_conn.put_object(Body=file.read(), Bucket=bucket_name, Key=file_key)
        region = os.environ.get('REGION')
        # file_url = f"s3://{bucket_name}/{file_key}"
        file_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{file_key}"
        return str(file_url)
    except Exception as e:
        return False
    
def get_content_type(filename):
        content_type = filename.split('.')[-1]
        if content_type == 'png': 
            content_type = 'image/png'
        elif content_type == 'jpg' or content_type == 'jpeg':
            content_type = 'image/jpeg'
        elif content_type == 'pdf':
            content_type = 'application/pdf'
        elif content_type == 'txt':
            content_type = 'text/plain'
        elif content_type == 'docx':
            content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        return content_type

def create_presigned_url(filename, doc_type, content_type, expiration=3600):
    s3_client = make_s3_connection()

    if doc_type == "kyc":
        bucket_name = Constants.BUCKET_FOR_KYC
        object_name = f"KYC_documents/{filename}"
    elif doc_type == "other":
        bucket_name = Constants.BUCKET_FOR_FINANCE_DOCUMENTS
        object_name = f"finance_documents/{filename}"
    elif doc_type == "photos":
        bucket_name = Constants.BUCKET_FOR_PHOTOGRAPHS_DOCUMENTS
        object_name = f"photographs/{filename}"
    elif doc_type == 'profile-photo':
        bucket_name = Constants.BUCKET_FOR_PROFILE_PHOTOS
        object_name = f"Profile_photos/{filename}"

    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name,
                                                            'ResponseContentDisposition': 'inline',
                                                            'ResponseContentType': content_type,
                                                    },
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    return response


def generate_empID():
    
    from user_auth.models import User
    
    if User.objects.exists():
        users_with_new_format = User.objects.filter(emp_id__regex=r'^EMP\d{4}$')
        if users_with_new_format:
            last_user = users_with_new_format.order_by('-emp_id').first()
            last_sequence = int(last_user.emp_id[3:])
        else:
            last_sequence = 0
    else:
        last_sequence = 0

    emp_id = "EMP" + (last_sequence + 1).__str__().zfill(4)

    return emp_id


def generate_leadID():
    """Generate a Lead_id of specified format: LEAD0001, LEAD0002, and so on."""

    from leads.models import Leads 

    if Leads.objects.exists():
        lead_with_new_format = Leads.objects.filter(lead_id__regex=r'^LEAD\d{4}$')
        if lead_with_new_format:
            last_lead = lead_with_new_format.order_by('-lead_id').first()
            last_sequence = int(last_lead.lead_id[4:])
        else:
            last_sequence = 0
    else:
        last_sequence = 0

    lead_id = "LEAD" + (last_sequence + 1).__str__().zfill(4)

    return lead_id

def generate_applicationID():
    """Generate a applicante_id of specified format: APP0001, APP0002, and so on."""
    
    from applicants.models import Applicants

    if Applicants.objects.exists():
        applicants_with_new_format = Applicants.objects.filter(application_id__regex=r'^APP\d{4}$')
        if applicants_with_new_format:
            last_applicant = applicants_with_new_format.order_by('-application_id').first()
            last_sequence = int(last_applicant.application_id[3:])            
        else:
            last_sequence = 0
    else:
        last_sequence = 0

    applicant_id = "APP" + (last_sequence + 1).__str__().zfill(4)

    return applicant_id

def generate_customerID():
    """Generate a applicante_id of specified format: CUST0001, CUST0002, and so on."""
    
    from customer.models import CustomerDetails 

    if CustomerDetails.objects.exists():
        customers_with_new_format = CustomerDetails.objects.filter(cif_id__regex=r'^CUST\d{4}$')
        if customers_with_new_format:
            last_customer = customers_with_new_format.order_by('-cif_id').first()
            last_sequence = int(last_customer.cif_id[4:])
        else:
            last_sequence = 0
    else:
        last_sequence = 0

    customer_id = "CUST" + (last_sequence + 1).__str__().zfill(4)

    return customer_id


def generate_PaymentID(length=8):
    """Generate a random payment of specified length."""

    Payment_id = "pmt_" + "".join(random.choices(string.digits, k=length))
    return Payment_id

def generate_locanID(length=8):
    """Generate a random payment of specified length."""

    loan_id = "ln_" + "".join(random.choices(string.digits, k=length))
    return loan_id

def generate_CollateralID(length=8):
    """Generate a random payment of specified length."""

    Collateral_id = "cltrl_" + "".join(random.choices(string.digits, k=length))
    return Collateral_id

def generate_cafID(length=8):
    """Generate a random caf of specified length."""

    caf_id = "caf_" + "".join(random.choices(string.digits, k=length))
    return caf_id

def generate_OrderID(length=8):
    """Generate a random payment of specified length."""

    Collateral_id = "ord_" + "".join(random.choices(string.digits, k=length))
    return Collateral_id

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

def generate_agent_code(prefix='dke_', length=4):
    random_numbers = ''.join(random.choices(string.digits, k=length))
    return prefix + random_numbers

def save_comment(comment_text):
    
    from user_auth.serializers import CommentSerializer
    from user_auth.models import Comments 
    
    if comment_text:
        serializer = CommentSerializer(data={"comment":comment_text})
        if serializer.is_valid():
            obj = serializer.save()
            return Comments.objects.get(pk=obj.pk)
        else:
            return False
    else:
        return False
