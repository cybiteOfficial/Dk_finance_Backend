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
from customer.models import CustomerDetails, CustomerAddress
from customer.serializers import CustomerDetailsSerializer, AddressSerializer
from kyc.models import DocumentsUpload
from kyc.serializers import DocumentUploadSerializer
from loan.models import Loan
from loan.serializers import LoanSerializer
from error_logs.models import UserLog
from user_auth.models import User

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
        for obj in serializer.data:
                if obj['documentUpload']:
                    fileurl = obj['documentUpload']
                    filename = fileurl.split('/')[-1]
                    content_type = get_content_type(filename)
                    obj['documentUpload'] = create_presigned_url(filename=filename, doc_type='kyc',\
                                                        content_type=content_type, expiration=3600
                                                    )
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
    
    def get_customer_details(self, application_id):
        data = []
        
        if application_id:
            customer_queryset = CustomerDetails.objects.filter(applicant_id = application_id)
            
            for customer in customer_queryset:
                current_address = CustomerAddress.objects.get(customer_id = customer.uuid, is_current = True, is_permanent = False) if CustomerAddress.objects.filter(customer_id = customer.uuid, is_current = True, is_permanent = False).exists() else None
                permanent_address = CustomerAddress.objects.get(customer_id = customer.uuid, is_current = False, is_permanent = True) if CustomerAddress.objects.filter(customer_id = customer.uuid, is_current = False, is_permanent = True).exists() else None
                data.append({
                    'details': CustomerDetailsSerializer(customer).data,
                    'current_address': AddressSerializer(current_address).data,
                    'permanent_address': AddressSerializer(permanent_address).data,
                })
                
        return data


    def get(self, request):
        application_id = request.query_params.get('application_id')

        if Applicants.objects.filter(application_id = application_id).exists():
            
            application_id = Applicants.objects.get(application_id = application_id).pk 
            
            customer_details = self.get_customer_details(application_id=application_id)

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
            "customer_details": customer_details,
            "loan_details": loan_details,
            "caf_details": caf_details,
            "collateral_details": collateral_details,
            "document_details_other": other_document_details,
            "document_details_photos": photos_document_details,
        }
        
        # Logs
        logged_user = User.objects.get(username=request.user.username)
        api = 'GET api/v1/print_document'
        details = f'sanctioned letter for {request.query_params.get("application_id")}'
        UserLog.objects.create(
            user=logged_user, 
            api=api,
            details=details, 
            applicant_id=application_id
        )

        return Response(
            response_data(False, "Details found", data),
            status=status.HTTP_200_OK
        )
