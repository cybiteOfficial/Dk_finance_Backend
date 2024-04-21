from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils import response_data, make_s3_connection, upload_file_to_s3_bucket
from leads.models import Leads
from .models import KYCDetails, DocumentsUpload
from .serializers import KycDetailsSerializer, DocumentUploadSerializer
from constant import Constants

class KYCVIew(APIView):
    serializer_class = KycDetailsSerializer
    permission_classes = (IsAuthenticated,)
    queryset = KYCDetails.objects.all()

    def get_kyc_object(self, pk):
        try:
            return self.queryset.get(pk=pk)
        except KYCDetails.DoesNotExist:
            return None
    
    def post(self, request):
        data = request.data.copy()
        for field in ["first_name", "last_name"]:
            if request.data.get(field):
                data[field] = request.data[field].capitalize()
                
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                response_data(False, "KYC created successfully", serializer.data),
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                response_data(True, "Something went wrong", serializer.errors),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request):
        try:
            # lead_id = request.query_params.get('lead_id')
            kyc_objs = self.queryset.filter(lead__lead_id = lead_id)
            if kyc_objs:
                serializer = self.serializer_class(kyc_objs, many=True)
                return Response(
                    response_data(False, "Sucess", serializer.data), status.HTTP_200_OK
                )
            else:
                return Response(
                response_data(True, "Does not contains any KYC details for this lead."), status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                response_data(True, "Something went wrong"), status.HTTP_400_BAD_REQUEST
            )
        
    def put(self, request):
        try:
            kyc_id = request.query_params.get('kyc_id')
            kyc_obj = self.get_kyc_object(kyc_id)

            if kyc_obj:
                serializer = self.serializer_class(kyc_obj, request.data, partial=True)
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
                        response_data(True, "Kyc Object Not Found."),
                        status=status.HTTP_200_OK,
                    )
        except Exception as e:
            return Response(
                response_data(True, "Something went wrong.", e),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request):
        kyc_id = request.query_params.get('kyc_id')
        kyc_obj = self.get_kyc_object(kyc_id)
        if kyc_obj :
            if not request.user.is_superuser:
                return Response(
                    response_data(True, "Permission denied for the user."),
                    status.HTTP_401_UNAUTHORIZED,
                )
            kyc_obj.delete()
            return Response(response_data(False, "KYC details Deleted."), status.HTTP_200_OK)
        else:
            return Response(response_data(True, "KYC object not found."), status.HTTP_200_OK)


class DocumentsUploadVIew(APIView):
    serializer_class = DocumentUploadSerializer
    permission_classes = (IsAuthenticated,)
    queryset = DocumentsUpload.objects.all()

    def get_document_object(self, pk):
        try:
            return self.queryset.get(pk=pk)
        except DocumentsUpload.DoesNotExist:
            return None
    
    def post(self, request):
        data = request.data.copy()
        kyc_id = data.get('kyc_id', None)
        file_obj = request.FILES.get('file')
        if data.get('document_type') == 'kyc' and kyc_id:
            if KYCDetails.objects.filter(pk=kyc_id).exists():  
                kyc_obj = KYCDetails.objects.get(pk=kyc_id)
                data['kyc'] = kyc_obj.pk
                data['document_name'] = data.get('document_name').capitalize()
                file_path = f"KYC_documents/{file_obj}"
                bucket_name = Constants.BUCKET_FOR_KYC
            else:
                return Response(
                    response_data(True, "KYC details not found"), status.HTTP_400_BAD_REQUEST
                )
        else:
            file_path = f"finance_documents/{file_obj}"
            bucket_name = Constants.BUCKET_FOR_FINANCE_DOCUMENTS

        s3_conn = make_s3_connection()
        file_url = upload_file_to_s3_bucket(
            s3_conn, file_obj, bucket_name, file_path
        )
        if file_url:
            data["file"] = file_url
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    response_data(False, "Document uploaded successfully", serializer.data),
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    response_data(True, "Something went wrong", serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST,
                )