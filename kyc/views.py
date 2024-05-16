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

    def save_document(self, file, data, doc_type, obj=False):
        if doc_type == "kyc":
            file_path = f"KYC_documents/{file}"
            bucket_name = Constants.BUCKET_FOR_KYC
        elif doc_type == "other":
            file_path = f"finance_documents/{file}"
            bucket_name = Constants.BUCKET_FOR_FINANCE_DOCUMENTS
        elif doc_type == "photos":
            file_path = f"photographs/{file}"
            bucket_name = Constants.BUCKET_FOR_PHOTOGRAPHS_DOCUMENTS
        else:
            ...
        s3_conn = make_s3_connection()
        file_url = upload_file_to_s3_bucket(
            s3_conn, file, bucket_name, file_path
        )
        if file_url:
            data["file"] = file_url
        if obj  :
            serializer = self.serializer_class(obj ,data=data, partial=True)
        else:
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
                    data['kyc'] = kyc_obj.pk
                    document_res = self.save_document(data.get('file'), data, data.get('document_type'))
                    response.append(document_res)
                    KYCDetails.objects.filter(pk = kyc_id).update(kyc_document_verified=True)
                else:
                    return Response(
                        response_data(True, "KYC details not found"), status.HTTP_400_BAD_REQUEST
                    )
                
            elif app_id:
                if Applicants.objects.filter(application_id = app_id).exists():
                    applicant = Applicants.objects.get(application_id = app_id)
                    data['application'] = applicant.pk
                    document_res = self.save_document(data.get('file'), data, data.get('document_type'))
                    response.append(document_res)        
                else:
                    return Response(
                        response_data(True, "Applicant not found"), status.HTTP_400_BAD_REQUEST
                    )
                
            return Response(
                response_data(False, "Document uploaded successfully", response),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                response_data(True, str(e)),
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    def get(self, request):
        application_id = request.query_params.get('application_id')
        kyc_id = request.query_params.get('kyc_id')
        document_type = request.query_params.get('document_type')
        if application_id:
            data = self.queryset.filter(application__application_id = application_id,document_type = document_type)
        elif kyc_id:
            data = self.queryset.filter(kyc__uuid = kyc_id,document_type = 'kyc')
        else:
            return Response(
                response_data(True, "Please pass kyc or application id"), status.HTTP_400_BAD_REQUEST
            )
        serializer = self.serializer_class(data, many=True  )
        if serializer:
            return Response(
            response_data(False, "Documents Lists", serializer.data),
            status=status.HTTP_200_OK,
        )
        else:
            return Response(
                response_data(True, "Something went wrong"),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request):
        data = request.data.copy()
        
        documents_data = eval(data.get('documents'))
        response = []
        for doc_data in documents_data:
            doc_data= {k: v for k, v in doc_data.items() if k not in ['application', 'kyc']}
            if self.queryset.filter(uuid=doc_data['uuid']).exists():
                queryset = self.queryset.get(uuid=doc_data['uuid'])
                if isinstance(data['file'], str):
                    serializer = self.serializer_class(queryset)
                    response.append(serializer.data)
                else:
                    document_res = self.save_document(doc_data.get('file'), doc_data, doc_data.get('document_type'), queryset)
                    if document_res:
                        response.append(document_res)
                    else:
                        return Response(
                            response_data(True, "Something went wrong.", serializer.errors),
                            status=status.HTTP_400_BAD_REQUEST,
                        )
        return Response(
            response_data(False, "Successfully updated.", response),
            status.HTTP_200_OK,
        )
        