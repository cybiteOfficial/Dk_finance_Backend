from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from utils import response_data, get_content_type, create_presigned_url

from applicants.models import Applicants
from collateral_details.models import CollateralDetails
from collateral_details.serializers import CollateralDetailsSerializer
from customer_application.models import CustomerApplicationForm
from customer_application.serializers import CafSerializer
from kyc.models import DocumentsUpload
from kyc.serializers import DocumentUploadSerializer
from loan.models import Loan
from loan.serializers import LoanSerializer

class PrintDocumentView(APIView):

    def get_loan_details(self, application_id):
        loans_queryset = Loan.objects.filter(applicant_id = application_id)
        serializer = LoanSerializer(loans_queryset, many=True)
        return serializer.data
    
    def get_caf_details(self, application_id):
        caf_queryset = CustomerApplicationForm.objects.filter(applicant_id = application_id)
        serializer = CafSerializer(caf_queryset, many=True)
        return serializer.data
    
    def get_collateral_details(self, application_id):
        collateral_queryset = CollateralDetails.objects.filter(applicant_id = application_id)
        serializer = CollateralDetailsSerializer(collateral_queryset, many=True)
        return serializer.data
    
    def get_document_details(self, document_type, application_id):
        if application_id:
            document_queryset = DocumentsUpload.objects.filter(application_id = application_id, document_type = document_type)
            serializer = DocumentUploadSerializer(document_queryset, many=True)
            for obj in serializer.data:
                if obj['file']:
                    fileurl = obj['file']
                    filename = fileurl.split('/')[-1]
                    content_type = get_content_type(filename)
                    obj['file'] = create_presigned_url(filename=filename, doc_type=obj['document_type'],\
                                                        content_type=content_type, expiration=3600
                                                    )

        return serializer.data


    def get(self, request):
        application_id = request.query_params.get('application_id')
        kyc_id = request.query_params.get('kyc_id')

        if Applicants.objects.filter(application_id = application_id).exists():
            
            application_id = Applicants.objects.get(application_id = application_id).pk 

            # Loan details
            loan_details = self.get_loan_details(application_id=application_id)

            # CAF details
            caf_details = self.get_caf_details(application_id=application_id)

            # Collateral details
            collateral_details = self.get_collateral_details(application_id=application_id)

            # Document details
            other_document_details = self.get_document_details(document_type='other', application_id=application_id)
            photos_document_details = self.get_document_details(document_type='photos', application_id=application_id)

        else:
            return Response(
                response_data(True, "Application id not found."),
                status=status.HTTP_400_BAD_REQUEST
            )

        data = {
            "loan_details": loan_details,
            "caf_details": caf_details,
            "collateral_details": collateral_details,
            "document_details_other": other_document_details,
            "document_details_photos": photos_document_details,
        }

        return Response(
            response_data(False, "Details found", data),
            status=status.HTTP_200_OK
        )
