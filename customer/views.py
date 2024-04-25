from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomerDetails
from .serializers import CustomerDetailsSerializer

from applicants.models import Applicants
from constant import Constants
from utils import response_data, make_s3_connection, upload_file_to_s3_bucket, save_comment
from rest_framework import status
from pagination import CommonPagination

class CustomerDetailsAPIView(generics.ListCreateAPIView):
    queryset = CustomerDetails.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerDetailsSerializer
    pagination_class = CommonPagination

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
            if customer_id:
                customer_obj = self.get_customer(customer_id)
                if customer_obj:
                    paginator = self.pagination_class()
                    paginated_res = paginator.paginate_queryset([customer_obj], request)
                    serializer = self.serializer_class(paginated_res, many=True)
                    return paginator.get_paginated_response(serializer.data)
                else:
                    return Response(
                    response_data(True, "Customer details does not exits."), status.HTTP_200_OK
                )
            elif application_id:
                customer_objs = self.get_customer_by_appID(application_id)
                if customer_objs:
                    paginator = self.pagination_class()
                    paginated_res = paginator.paginate_queryset(customer_objs, request)
                    serializer = self.serializer_class(paginated_res, many=True)
                    return paginator.get_paginated_response(serializer.data)
                else:
                    return Response(
                        response_data(True, "Customer not found for this application ID."), status.HTTP_200_OK
                    )
        except Exception as e:
            return Response(
                response_data(True, "Something went wrong"), status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):

        data = request.data.copy()
        if Applicants.objects.filter(application_id = request.data['application_id']).exists():
            applicant = Applicants.objects.get(application_id = request.data['application_id'])
            data['applicant'] = applicant.pk
        else:
            return Response(
                response_data(True, "Applicant not found"), status.HTTP_400_BAD_REQUEST
            )
        try:
            if request.data.get('profile_photo'):
                file_obj = request.FILES.get('profile_photo')
                bucket_name = Constants.BUCKET_FOR_PROFILE_PHOTOS
                file_path = f"Profile_photos/{file_obj}"
                s3_conn = make_s3_connection()
                file_url = upload_file_to_s3_bucket(
                    s3_conn, file_obj, bucket_name, file_path
                )
                if file_url:
                    data['profile_photo'] = file_url
            comment = save_comment(data['comment'])
            if comment:
                data['comment'] = comment.pk
            serializer = self.serializer_class(data=data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(
                    response_data(False, "Customer created successfully", serializer.data),
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    response_data(True, "Something went Wrong"), status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                response_data(True, e, serializer.errors),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request):
        try:
            data = request.data.copy()
            customer_id = request.query_params.get('customer_id')
            customer_obj = self.get_customer(customer_id)

            if customer_obj:
                if request.data.get('profile_photo'):
                    file_obj = request.FILES.get('profile_photo')
                    bucket_name = Constants.BUCKET_FOR_PROFILE_PHOTOS
                    file_path = f"Profile_photos/{file_obj}"
                    s3_conn = make_s3_connection()
                    file_url = upload_file_to_s3_bucket(
                        s3_conn, file_obj, bucket_name, file_path
                    )
                    if file_url:
                        data['profile_photo'] = file_url

                serializer = self.serializer_class(customer_obj, data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        response_data(False, "Successfully updated.", serializer.data),
                        status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        response_data(True, "Something went wrong.", serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                        response_data(True, "Customer Object Not Found."),
                        status=status.HTTP_200_OK,
                    )
        except Exception as e:
            return Response(
                response_data(True, "Something went wrong.", e),
                status=status.HTTP_400_BAD_REQUEST,
            )
