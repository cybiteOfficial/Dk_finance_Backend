from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils import response_data, make_s3_connection, upload_file_to_s3_bucket, save_comment
from leads.models import Leads
from .models import KYCDetails, DocumentsUpload
from .serializers import KycDetailsSerializer, DocumentUploadSerializer
from constant import Constants
from applicants.models import Applicants

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
        lead_id = request.data.get('lead_id')
        if Leads.objects.filter(lead_id=lead_id).exists():
            lead_obj = Leads.objects.get(lead_id=lead_id)
            data['lead_id'] = lead_obj.pk
        for field in ["first_name", "last_name"]:
            if request.data.get(field):
                data[field] = request.data[field].capitalize()

        comment = save_comment(data.get('comment'))
        if comment:
            data['comment'] = comment.pk

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
            lead_id = request.query_params.get('lead_id')
            kyc_objs = self.queryset.filter(lead_id__lead_id=lead_id)
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

    def save_document(self, file, data, doc_type):
        if doc_type == "kyc":
            file_path = f"KYC_documents/{file}"
            bucket_name = Constants.BUCKET_FOR_KYC
        if doc_type == "other":
            file_path = f"finance_documents/{file}"
            bucket_name = Constants.BUCKET_FOR_FINANCE_DOCUMENTS
            ...
        s3_conn = make_s3_connection()
        file_url = upload_file_to_s3_bucket(
            s3_conn, file, bucket_name, file_path
        )
        if file_url:
            data["file"] = file_url
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            return False

    def post(self, request):
        try:
            data = request.data.copy()
            kyc_id = data.get('kyc_id', None)
            app_id = data.get('application_id', None)
            response = []
            if data.get('document_type') == 'kyc' and kyc_id:
                if KYCDetails.objects.filter(pk=kyc_id).exists():
                    kyc_obj = KYCDetails.objects.get(pk=kyc_id)
                    for doc_data in eval(data.get('documents')):
                        doc_data['kyc'] = kyc_obj.pk
                        doc_data['document_name'] = doc_data.get('document_name').capitalize()
                        doc_data['document_type'] = data.get('document_type')
                        document_res = self.save_document(data.get('file'), doc_data, data.get('document_type'))
                        response.append(document_res)
                    KYCDetails.objects.filter(pk = kyc_id).update(kyc_document_verified=True)
                else:
                    return Response(
                        response_data(True, "KYC details not found"), status.HTTP_400_BAD_REQUEST
                    )
            elif app_id:

                if Applicants.objects.filter(application_id = app_id).exists():
                    applicant = Applicants.objects.get(application_id = app_id)
                    for doc_data in eval(data.get('documents')):
                        doc_data['application'] = applicant.pk
                        doc_data['document_name'] = doc_data.get('document_name').capitalize()
                        doc_data['document_type'] = data.get('document_type')
                        document_res = self.save_document(data.get('file'), doc_data, data.get('document_type'))                
                        response.append(document_res)
                else:
                    return Response(
                        response_data(True, "Applicant not found"), status.HTTP_400_BAD_REQUEST
                    )
            return Response(
                response_data(False, "Document uploaded successfully", response),
                status=status.HTTP_200_OK,
            )
        except:
            return Response(
                response_data(True, "Something went wrong"),
                status=status.HTTP_400_BAD_REQUEST,
            )