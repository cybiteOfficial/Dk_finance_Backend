from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import CollateralDetails
from .serializers import CollateralDetailsSerializer
from applicants.models import Applicants
from constant import Constants
from utils import response_data, save_comment, make_s3_connection, upload_file_to_s3_bucket, get_content_type, create_presigned_url
from Dev_Kripa_Finance.settings.base import MAX_UPLOAD_SIZE
from error_logs.models import UserLog
from user_auth.models import User

class CollateralDetailsAPIView(APIView):
    serializer_class = CollateralDetailsSerializer
    permission_classes = (IsAuthenticated,)
    queryset = CollateralDetails.objects.all()

    def get_collateral_detail(self, pk):
        try:
            return self.queryset.get(collateral_id=pk)
        except CollateralDetails.DoesNotExist:
            return None
    
    def post(self, request):
        data = request.data.copy()
        data.pop('documentUpload', None)
        collateral_id = request.data.get('collateral_id')
        application_id = request.data.get('applicant_id')
        if Applicants.objects.filter(application_id = application_id).exists():
            applicant = Applicants.objects.get(application_id = application_id)
            data['applicant'] = applicant.pk
        else:
            return Response(
                response_data(True, "Applicant not found"), status.HTTP_400_BAD_REQUEST
            )

        comment = save_comment(request.data.get('comment'))
        if comment:
            data['comment'] = comment.pk
            
        if request.FILES.get('documentUpload'):
            file_obj = request.FILES.get('documentUpload')
            if file_obj.size > MAX_UPLOAD_SIZE:
                return Response(
                    response_data(True, "File size too large."),
                    status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                )
            bucket_name = Constants.BUCKET_FOR_KYC
            file_path = f"collatral_doc/{file_obj}"
            s3_conn = make_s3_connection()
            file_url = upload_file_to_s3_bucket(
                s3_conn, file_obj, bucket_name, file_path
            )
            if file_url:
                data['documentUpload'] = file_url

        if collateral_id:

            if CollateralDetails.objects.filter(collateral_id=collateral_id).exists():
                collateral_obj = CollateralDetails.objects.get(collateral_id=collateral_id)
                serializer = self.serializer_class(collateral_obj, data=data)
            else:
                serializer = self.serializer_class(data=data)
               
        else:
            serializer = self.serializer_class(data=data)

        try:
            if serializer.is_valid():
                serializer.save()

                # Logs
                logged_user = User.objects.get(username=request.user.username)
                api = 'POST api/v1/collateral_details'
                details = f'created collateral details for {application_id}'
                applicant = Applicants.objects.get(application_id = application_id)
                UserLog.objects.create(
                    user=logged_user, 
                    api=api,
                    details=details, 
                    applicant_id=applicant.pk
                )
                
                return Response(
                    response_data(False, "success", serializer.data),
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    response_data(True, "Something went wrong", serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                response_data(True, e, serializer.errors),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request):
        try:
            collateral_id = request.query_params.get('collateral_id', None)
            application_id = request.query_params.get('application_id', None)

            if Applicants.objects.filter(application_id = application_id).exists():
                collateral_obj = self.queryset.filter(applicant__application_id=application_id)
                serializer = self.serializer_class(collateral_obj, many=True)
                for obj in serializer.data:
                    file_url = obj['documentUpload']
                    if file_url:
                        filename = file_url.split('/')[-1]
                        content_type = get_content_type(filename=filename)
                        s3_client = make_s3_connection()
                        presigned_url = s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': Constants.BUCKET_FOR_KYC,
                                                                'Key': f"collatral_doc/{filename}",
                                                                'ResponseContentDisposition': 'inline',
                                                                'ResponseContentType': content_type,
                                                        },
                                                        ExpiresIn=3600)
                        obj['documentUpload'] = presigned_url
                
                # Logs
                logged_user = User.objects.get(username=request.user.username)
                api = 'GET api/v1/collateral_details'
                details = f'viewed collateral details for {application_id}'
                applicant = Applicants.objects.get(application_id = application_id)
                UserLog.objects.create(
                    user=logged_user, 
                    api=api,
                    details=details, 
                    applicant_id=applicant.pk
                )
                    
                return Response(
                    response_data(False, "collateral details found", serializer.data),
                    status=status.HTTP_200_OK,
                )
            
            
            if collateral_id:
                if self.queryset.filter(collateral_id=collateral_id).exists():
                    collateral_obj = self.queryset.get(collateral_id=collateral_id)
                    serializer = self.serializer_class(collateral_obj)
                    
                    # Logs
                    logged_user = User.objects.get(username=request.user.username)
                    api = 'GET api/v1/collateral_details'
                    details = f'viewed collateral details for {collateral_id}'
                    applicant = Applicants.objects.get(application_id = application_id)
                    UserLog.objects.create(
                        user=logged_user, 
                        api=api,
                        details=details, 
                        applicant_id=applicant.pk
                    )
                
                    return Response(
                        response_data(False, "collateral details found", serializer.data),
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        response_data(True, "Collatral not found."),
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                return Response(
                    response_data(True, "Collateral detail not found"),
                    status=status.HTTP_404_NOT_FOUND,
                )
                
        except Exception as e:
            return Response(
                response_data(True, e),
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request):
        collateral_id = request.query_params.get('collateral_id')
        collateral = CollateralDetails.objects.get(collateral_id=collateral_id)
        if collateral:
            serializer = self.serializer_class(collateral, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                
                # Logs
                logged_user = User.objects.get(username=request.user.username)
                api = 'PUT api/v1/collateral_details'
                details = f'viewed collateral details for {collateral_id}'
                application_id = serializer.data['applicant']
                applicant = Applicants.objects.get(application_id = application_id)
                UserLog.objects.create(
                    user=logged_user, 
                    api=api,
                    details=details, 
                    applicant_id=applicant.pk
                )
                
                return Response(
                    response_data(False, "Collateral detail updated successfully", serializer.data),
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    response_data(True, "Something went wrong", serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                response_data(True, "Collateral detail not found"),
                status=status.HTTP_404_NOT_FOUND,
            )

    def delete(self, request, collateral_id):
        collateral_detail = self.get_collateral_detail(collateral_id)
        if collateral_detail:
            collateral_detail.delete()
            return Response(response_data(False, "Collateral detail deleted."), status.HTTP_200_OK)
        else:
            return Response(response_data(True, "Collateral detail not found."), status.HTTP_404_NOT_FOUND)
