from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils import response_data, make_s3_connection, upload_file_to_s3_bucket, save_comment, create_presigned_url, get_content_type
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

    def save_document(self, file, data, doc_type, previous_data=False):
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
        if previous_data:
            serializer = self.serializer_class(previous_data, data=data, partial=True)
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
            documents = data.get('documents')
            document_type = data.get('document_type')
            comment = save_comment(data.get('comment'))
        
            
            files = []
            for uploaded_file in data.getlist('file'):
                files.append(uploaded_file)

            response = []
            file_num = 0
            if document_type == 'kyc' and kyc_id:
                if KYCDetails.objects.filter(pk=kyc_id).exists():
                    kyc_obj = KYCDetails.objects.get(pk=kyc_id)
                    for document in eval(documents):
                        document['kyc'] = kyc_obj.pk
                        document['document_type'] = document_type
                        document['description'] = data.get('description')
                        if comment:
                            document['comment'] = comment.pk
                        document_res = self.save_document(files[file_num], document, document['document_type'])
                        response.append(document_res)  
                        file_num += 1
                    KYCDetails.objects.filter(pk = kyc_id).update(kyc_document_verified=True)
                else:
                    return Response(
                        response_data(True, "KYC details not found"), status.HTTP_400_BAD_REQUEST
                    )
                
            elif app_id:
                if Applicants.objects.filter(application_id = app_id).exists():
                    applicant = Applicants.objects.get(application_id = app_id)
                    if document_type == 'other':
                        for document in eval(documents):
                            document['application'] = applicant.pk
                            document['document_type'] = document_type
                            document['description'] = data.get('description')
                            if comment:
                                document['comment'] = comment.pk
                            document_res = self.save_document(files[file_num], document, document['document_type'])
                            response.append(document_res)
                            file_num += 1
                    elif document_type == 'photos':
                        for i in range(len(files)):
                            data['application'] = applicant.pk
                            data['document_type'] = document_type
                            data['description'] = data.get('description')
                            if comment:
                                data['comment'] = comment.pk
                            document_res = self.save_document(files[file_num], data, data['document_type'])
                            response.append(document_res)
                            file_num += 1

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

        serializer = self.serializer_class(data, many=True)
        for file in serializer.data:
            file_url = file['file']
            filename = file_url.split('/')[-1]
            content_type = get_content_type(filename=filename)
            presigned_url = create_presigned_url(filename=filename, doc_type=file['document_type'], content_type=content_type)
            file['file'] = presigned_url

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
        data = request.data
        document_type = request.query_params.get('document_type')

        documents = data.get('documents')
        comment = save_comment(data.get('comment'))

        response = []
        files = []
        for uploaded_file in data.getlist('file'):
            files.append(uploaded_file)
        file_num = 0

        for doc in eval(documents):
            document_uuid = doc['uuid']
            if DocumentsUpload.objects.filter(uuid = document_uuid).exists():
                file_updated = doc['file_updated'].strip().lower() == 'true'
                
                if not file_updated:
                    doc['description'] = data.get('description')
                    if comment:
                        doc['comment'] = comment.pk
                    serializer = self.serializer_class(instance=DocumentsUpload.objects.get(uuid = document_uuid), data=doc, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        response.append(serializer.data)

                else:
                    doc['description'] = data.get('description')
                    if comment:
                        doc['comment'] = comment.pk
                    document_res = self.save_document(files[file_num], doc, document_type, previous_data=DocumentsUpload.objects.get(uuid = document_uuid))
                    response.append(document_res)
                    file_num += 1   

            else:
                return Response(
                    response_data(True, "Document not found"),
                    status=status.HTTP_400_BAD_REQUEST,
                )    
        
        return Response(
            response_data(False, "Document uploaded successfully", response),
            status=status.HTTP_200_OK,
        )
    
    def delete(self, request):
        
        document_uuid = request.data.get('document_uuid')
        
        if DocumentsUpload.objects.filter(uuid = document_uuid).exists():
            document = DocumentsUpload.objects.get(uuid = document_uuid)
            document.delete()
            return Response(
                response_data(False, "Document deleted successfully"),
                status=status.HTTP_200_OK,
            )
        
        return Response(
            response_data(True, "Document not found"),
            status=status.HTTP_404_NOT_FOUND,
        )
