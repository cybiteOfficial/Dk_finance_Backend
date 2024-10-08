from rest_framework import generics
import json
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomerDetails, CustomerAddress, CustomerKYCDetails
from .serializers import CustomerDetailsSerializer, CustomCustomerSerializer, AddressSerializer, KYCSDetailsSerializer

from applicants.models import Applicants
from constant import Constants
from utils import response_data, make_s3_connection, upload_file_to_s3_bucket, save_comment, create_presigned_url, get_content_type
from rest_framework import status
from pagination import CommonPagination
from django.conf import settings
from user_auth.models import User
from error_logs.models import UserLog

class CustomerDetailsAPIView(generics.ListCreateAPIView):
    queryset = CustomerDetails.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerDetailsSerializer
    pagination_class = CommonPagination
    
    MAX_FILE_SIZE = settings.DATA_UPLOAD_MAX_MEMORY_SIZE

    def save_address(self, address_data):
        address_serializer = AddressSerializer(data=address_data)
        if address_serializer.is_valid():
            address_serializer.save()
            return address_serializer.data
        else:
            return False
    
    def update_address(self, address_obj , address_data):
        address_serializer = AddressSerializer(address_obj, address_data, partial=True)
        if address_serializer.is_valid():
            address_serializer.save()
            return address_serializer.data
        else:
            return False
        
    def get_customer(self, customer_id):
        try:
            return self.queryset.get(cif_id=customer_id)
        except CustomerDetails.DoesNotExist:
            return None
    
    def get_customer_by_appID(self, application_id):
        try:
            return self.queryset.filter(applicant__application_id = application_id)
        except CustomerDetails.DoesNotExist:
            return None
        
    def get(self, request):

        try:
            customer_id = request.query_params.get('customer_id')
            application_id = request.query_params.get('application_id')
            is_all = request.query_params.get('is_all')
            response = {}
            if customer_id:
                customer_obj = self.get_customer(customer_id)
                if customer_obj:
                    serializer = self.serializer_class(customer_obj)
                    customer_uuid = serializer.data['uuid']
                    
                    address_data = CustomerAddress.objects.filter(customer_id = customer_uuid)
                    file_url = serializer.data['profile_photo']
                    presigned_url = ''
                    if file_url:
                        filename = file_url.split('/')[-1]
                        content_type = get_content_type(filename=filename)
                        presigned_url = create_presigned_url(
                                                                filename=filename,
                                                                doc_type='profile-photo',
                                                                content_type=content_type
                                                            )
                    response['customer_data'] = serializer.data
                    response['customer_data']['profile_photo'] = presigned_url
                    if address_data:
                        for data in address_data:
                            if data.is_current == True and data.is_permanent == False:
                                address_serializer = AddressSerializer(data)
                                response['current_address'] = address_serializer.data
                            else:
                                address_serializer = AddressSerializer(data)
                                response['permanent_address'] = address_serializer.data
                                
                    try:
                        kyc = CustomerKYCDetails.objects.get(customer_id = customer_uuid)
                        if kyc:
                            kyc_serializer = KYCSDetailsSerializer(kyc)
                            aadhaar_file = kyc_serializer.data['aadhaar_file']
                            if aadhaar_file:
                                filename = aadhaar_file.split('/')[-1]
                                content_type = get_content_type(filename=filename)
                                aadhaar_file = create_presigned_url(
                                                            filename=filename,
                                                            doc_type='kyc',
                                                            content_type=content_type
                                                        )
                            pan_file = kyc_serializer.data['pan_file']
                            if pan_file:
                                filename = pan_file.split('/')[-1]
                                content_type = get_content_type(filename=filename)
                                pan_file = create_presigned_url(
                                                            filename=filename,
                                                            doc_type='kyc',
                                                            content_type=content_type
                                                        )
                            response['kyc_details'] = kyc_serializer.data
                            response['kyc_details']['aadhaar_file'] = aadhaar_file
                            response['kyc_details']['pan_file'] = pan_file
                    except:
                        response['kyc_details'] = None    
                                
                    # paginator = self.pagination_class()
                    # paginated_res = paginator.paginate_queryset([customer_obj], request)
                    # serializer = self.serializer_class(paginated_res, many=True)
                    # return paginator.get_paginated_response(serializer.data)
                    
                    # Logs
                    logged_user = User.objects.get(username=request.user.username)
                    api = 'GET api/v1/customers'
                    details = f'viewed customer details of {customer_id}'
                    applicant = Applicants.objects.get(application_id = serializer.data['applicant'])
                    UserLog.objects.create(
                        user=logged_user, 
                        api=api,
                        details=details, 
                        applicant_id=applicant.pk
                    )
                    
                    return Response(response_data(False, "customer data", response))
                else:
                    return Response(
                    response_data(True, "Customer details does not exits."), status.HTTP_200_OK
                )
            elif application_id:
                customer_objs = self.get_customer_by_appID(application_id)
                if customer_objs:
                    if is_all:
                        serializer = CustomCustomerSerializer(customer_objs, many=True)
                        return Response(response_data(False, "All customer with specific applicaiton", serializer.data))
                    else:
                        paginator = self.pagination_class()
                        paginated_res = paginator.paginate_queryset(customer_objs, request)
                        serializer = self.serializer_class(paginated_res, many=True)
                        for applicant in serializer.data:
                            file_url = applicant.get('profile_photo')
                            if file_url:
                                filename = file_url.split('/')[-1]
                                content_type = get_content_type(filename=filename)
                                presigned_url = create_presigned_url(
                                                                        filename=filename,
                                                                        doc_type='profile-photo',
                                                                        content_type=content_type
                                                                    )
                                applicant.update({'profile_photo': presigned_url})
                   
                            try:
                                applicant['kyc_verified'] = CustomerKYCDetails.objects.get(customer_id = applicant.get('uuid')).is_verified
                            except:
                                applicant['kyc_verified'] = False
                        
                        # Logs
                        logged_user = User.objects.get(username=request.user.username)
                        api = 'GET api/v1/customers'
                        details = f'viewed customer details for {application_id}'
                        applicant = Applicants.objects.get(application_id = application_id)
                        UserLog.objects.create(
                            user=logged_user, 
                            api=api,
                            details=details, 
                            applicant_id=applicant.pk
                        )
                    
                        return paginator.get_paginated_response(serializer.data)
                else:
                    return Response(
                        response_data(True, "Customer not found for this application ID."), status.HTTP_200_OK
                    )
        except Exception as e:
            return Response(
                response_data(True, str(e)), status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):

        data = request.data
        customer_data = eval(data.get('customer_data'))
        if Applicants.objects.filter(application_id = customer_data['application_id']).exists():
            applicant = Applicants.objects.get(application_id = customer_data['application_id'])
            customer_data['applicant'] = applicant.pk
        else:
            return Response(
                response_data(True, "Applicant not found"), status.HTTP_400_BAD_REQUEST
            )
        try:
            if request.FILES.get('profile_photo'):
                file_obj = request.FILES.get('profile_photo')
                if file_obj.size > self.MAX_FILE_SIZE:
                    return Response(
                        response_data(True, "File size too big"), status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
                    )

                bucket_name = Constants.BUCKET_FOR_PROFILE_PHOTOS
                file_path = f"Profile_photos/{file_obj}"
                s3_conn = make_s3_connection()
                file_url = upload_file_to_s3_bucket(
                    s3_conn, file_obj, bucket_name, file_path
                )
                if file_url:
                    customer_data['profile_photo'] = file_url
            comment = save_comment(customer_data.get('comment'))
            if comment:
                customer_data['comment'] = comment.pk
            serializer = self.serializer_class(data=customer_data)

            if serializer.is_valid():
                customer_obj = serializer.save()
                current_address = eval(data.get('current_address'))
                per_addr = data.get('permanent_address', None)
                permanent_address = eval(per_addr) if per_addr else None
                kyc_details = eval(data.get('kyc_details', None))
                current_address_serializer_data = {}
                permanent_address_serializer_data = {}
                kyc_details_serializer_data = {}
                if current_address:
                    current_address['customer'] = customer_obj.pk
                    current_address['is_current'] = True
                    current_address['is_permanent'] = False
                    current_address_serializer_data = self.save_address(current_address)
                
                if permanent_address:
                    permanent_address['customer'] = customer_obj.pk
                    permanent_address['is_current'] = False
                    permanent_address['is_permanent'] = True
                    permanent_address_serializer_data = self.save_address(permanent_address)
                    
                if kyc_details:
                    kyc_details['customer'] = customer_obj.pk
                    try:
                        if request.FILES.get('aadhaar_file'):
                            file_obj = request.FILES.get('aadhaar_file')
                            if file_obj.size > self.MAX_FILE_SIZE:
                                return Response(
                                    response_data(True, "File size too big"), status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
                                )

                            bucket_name = Constants.BUCKET_FOR_KYC
                            file_path = f"KYC_Documents/{file_obj}"
                            s3_conn = make_s3_connection()
                            file_url = upload_file_to_s3_bucket(
                                s3_conn, file_obj, bucket_name, file_path
                            )
                            if file_url:
                                kyc_details['aadhaar_file'] = file_url
                        else:
                            pass
                        if request.FILES.get('pan_file'):
                            file_obj = request.FILES.get('pan_file')
                            if file_obj.size > self.MAX_FILE_SIZE:
                                return Response(
                                    response_data(True, "File size too big"), status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
                                )

                            bucket_name = Constants.BUCKET_FOR_KYC
                            file_path = f"KYC_documents/{file_obj}"
                            s3_conn = make_s3_connection()
                            file_url = upload_file_to_s3_bucket(
                                s3_conn, file_obj, bucket_name, file_path
                            )
                            if file_url:
                                kyc_details['pan_file'] = file_url
                    except Exception as e:
                        return Response(
                            response_data(True, e), status.HTTP_400_BAD_REQUEST
                        )
                    kyc = KYCSDetailsSerializer(data=kyc_details)
                    if kyc.is_valid():
                        kyc.save()
                    kyc_details_serializer_data = kyc.data
                
                response = {
                    "customer_data": serializer.data,
                    "current_address": current_address_serializer_data if current_address_serializer_data else {},
                    "permanent_address": permanent_address_serializer_data if permanent_address_serializer_data else current_address_serializer_data,
                    "kyc_details": kyc_details_serializer_data if kyc_details_serializer_data else status.HTTP_400_BAD_REQUEST
                }
                
                # Logs
                logged_user = User.objects.get(username=request.user.username)
                api = 'POST api/v1/customers'
                details = f'created customer {serializer.data["cif_id"]}'
                applicant = Applicants.objects.get(application_id = customer_data['application_id'])
                UserLog.objects.create(
                    user=logged_user, 
                    api=api,
                    details=details, 
                    applicant_id=applicant.pk
                )
                
                return Response(
                    response_data(False, "Customer created successfully", response),
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    response_data(True, "Something went Wrong"), status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                response_data(True, str(e), serializer.errors),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request):
        try:
            data = request.data.copy()
            customer_data = json.loads(data.get('customer_data'))
            cur_addr = data.get('current_address')
            current_address = eval(cur_addr) if cur_addr else None
            per_addr = data.get('permanent_address', None)
            permanent_address = eval(per_addr) if per_addr else None
            customer_id = request.query_params.get('customer_id')
            kyc_details = eval(data.get('kyc_details')) if data.get('kyc_details') else None

            customer_obj = self.get_customer(customer_id)
            response = []
            if customer_obj:
                customer_data= {k: v for k, v in customer_data.items() if k not in ['applicant', 'comment']}

                if request.FILES.get('profile_photo'):
                    file_obj = request.FILES.get('profile_photo')
                    bucket_name = Constants.BUCKET_FOR_PROFILE_PHOTOS
                    file_path = f"Profile_photos/{file_obj}"
                    s3_conn = make_s3_connection()
                    file_url = upload_file_to_s3_bucket(
                        s3_conn, file_obj, bucket_name, file_path
                    )
                    if file_url:
                        customer_data['profile_photo'] = file_url
                serializer = self.serializer_class(customer_obj, customer_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    customer_serializer_data = serializer.data
                    
                if current_address.get('uuid'):
                    if CustomerAddress.objects.filter(uuid = current_address.get('uuid')).exists():
                        current_obj = CustomerAddress.objects.get(uuid = current_address.get('uuid'), is_current = True, is_permanent = False)
                        serializer = AddressSerializer(current_obj, current_address, partial=True)
                        if serializer.is_valid():
                            serializer.save()
                            current_address_serializer_data = serializer.data
                        else:
                            return Response(
                                response_data(True, "Current address is not updated", serializer.errors),
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                            
                if permanent_address.get('uuid'):
                    if CustomerAddress.objects.filter(uuid = permanent_address.get('uuid')).exists():
                        current_obj = CustomerAddress.objects.get(uuid = permanent_address.get('uuid'), is_current = False, is_permanent = True)
                        serializer = AddressSerializer(current_obj, permanent_address, partial=True)
                        if serializer.is_valid():
                            serializer.save()
                            permanent_address_serializer_data = serializer.data
                        else:
                            return Response(
                                response_data(True, "Permanent address is not updated", serializer.errors),
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                            
                if kyc_details.get('uuid'):
                    if CustomerKYCDetails.objects.filter(uuid = kyc_details.get('uuid')).exists():
                        
                        if request.FILES.get('aadhaar_file'):
                            file_obj = request.FILES.get('aadhaar_file')
                            bucket_name = Constants.BUCKET_FOR_KYC
                            file_path = f"KYC_documents/{file_obj}"
                            s3_conn = make_s3_connection()
                            file_url = upload_file_to_s3_bucket(
                                s3_conn, file_obj, bucket_name, file_path
                            )
                            if file_url:
                                kyc_details['aadhaar_file'] = file_url
                                
                        if request.FILES.get('pan_file'):
                            file_obj = request.FILES.get('pan_file')
                            bucket_name = Constants.BUCKET_FOR_KYC
                            file_path = f"KYC_documents/{file_obj}"
                            s3_conn = make_s3_connection()
                            file_url = upload_file_to_s3_bucket(
                                s3_conn, file_obj, bucket_name, file_path
                            )
                            if file_url:
                                kyc_details['pan_file'] = file_url
                        
                        current_obj = CustomerKYCDetails.objects.get(uuid = kyc_details.get('uuid'))
                        serializer = KYCSDetailsSerializer(current_obj, kyc_details, partial=True)
                        if serializer.is_valid():
                            serializer.save()
                            kyc_details_serializer_data = serializer.data
                        else:
                            return Response(
                                response_data(True, "KYC details not updated", serializer.errors),
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                            
                else:
                    kyc_details['customer'] = customer_obj.pk
                    try:
                        if request.FILES.get('aadhaar_file'):
                            file_obj = request.FILES.get('aadhaar_file')
                            if file_obj.size > self.MAX_FILE_SIZE:
                                return Response(
                                    response_data(True, "File size too big"), status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
                                )

                            bucket_name = Constants.BUCKET_FOR_KYC
                            file_path = f"KYC_Documents/{file_obj}"
                            s3_conn = make_s3_connection()
                            file_url = upload_file_to_s3_bucket(
                                s3_conn, file_obj, bucket_name, file_path
                            )
                            if file_url:
                                kyc_details['aadhaar_file'] = file_url
                        else:
                            pass
                        if request.FILES.get('pan_file'):
                            file_obj = request.FILES.get('pan_file')
                            if file_obj.size > self.MAX_FILE_SIZE:
                                return Response(
                                    response_data(True, "File size too big"), status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
                                )

                            bucket_name = Constants.BUCKET_FOR_KYC
                            file_path = f"KYC_documents/{file_obj}"
                            s3_conn = make_s3_connection()
                            file_url = upload_file_to_s3_bucket(
                                s3_conn, file_obj, bucket_name, file_path
                            )
                            if file_url:
                                kyc_details['pan_file'] = file_url
                    except Exception as e:
                        return Response(
                            response_data(True, e), status.HTTP_400_BAD_REQUEST
                        )
                    kyc = KYCSDetailsSerializer(data=kyc_details)
                    if kyc.is_valid():
                        kyc.save()
                    kyc_details_serializer_data = kyc.data
                
                response = {
                    'customer_details': customer_serializer_data,
                    'current_address': current_address_serializer_data,
                    'permanent_address': permanent_address_serializer_data,
                    'kyc_details': kyc_details_serializer_data
                }
                
                
                # Logs
                logged_user = User.objects.get(username=request.user.username)
                api = 'PUT api/v1/customers'
                details = f'updated customer details of {customer_id}'
                applicant = Applicants.objects.get(application_id = response['customer_details']['applicant'])
                UserLog.objects.create(
                    user=logged_user, 
                    api=api,
                    details=details, 
                    applicant_id=applicant.pk
                )
                
                return Response(
                    response_data(False, "Customer updated successfully.", response),
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                        response_data(True, "Customer Object Not Found."),
                        status=status.HTTP_200_OK,
                    )
        except Exception as e:
            return Response(
                response_data(True, "Something went wrong.", str(e)),
                status=status.HTTP_400_BAD_REQUEST,
            )


class KYCVerifyView(generics.ListCreateAPIView):
    def post(self, request):
        customer_id = request.query_params.get('customer_id')
        customer = CustomerDetails.objects.get(cif_id = customer_id).pk
        application_id = CustomerDetails.objects.get(cif_id = customer_id).applicant
        CustomerKYCDetails.objects.filter(customer_id=customer).update(is_verified=True)
        
        # Logs
        logged_user = User.objects.get(username=request.user.username)
        api = 'POST api/v1/verify_kyc'
        details = f'verified kyc of {customer_id}'
        applicant = Applicants.objects.get(application_id = application_id)
        UserLog.objects.create(
            user=logged_user, 
            api=api,
            details=details, 
            applicant_id=applicant.pk
        )
        
        return Response(
            response_data(False, "KYC Verified Successfully."),
            status=status.HTTP_200_OK,
        )