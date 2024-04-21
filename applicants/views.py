from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ApplicantsSerializer

from .models import Applicants
from leads.models import Leads
from phonepay.models import Payment

from utils import response_data

class ApplicantCreateAPIView(APIView):

    def get(self, request):
        try:
            application_id = request.query_params.get('application_id')
            applicant_obj = Applicants.objects.get(application_id = application_id)
            
            if applicant_obj:
                serializer = ApplicantsSerializer(applicant_obj, many= True)
                return Response(
                    response_data(False, "Sucess", serializer.data), status.HTTP_200_OK
                )
            else:
                return Response(
                response_data(True, "Not found any Applicant."), status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                response_data(True, e), status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        
        data = request.data.copy()

        lead_id = request.data.get('lead_id')
        if Leads.objects.filter(lead_id=lead_id).exists():  
            lead_obj = Leads.objects.get(lead_id=lead_id)
        else:
            return Response(
                response_data(True, "Lead not found"), status.HTTP_400_BAD_REQUEST
            )
        
        payment_id = request.data.get('payment_id')
        if Payment.objects.filter(payment_id=payment_id).exists():  
            payment_obj = Payment.objects.get(payment_id=payment_id)
            if payment_obj.status.lower() != "DONE":
                return Response(
                    response_data(True, "Payment is Pending"), status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                response_data(True, "Payment is not Done yet"), status.HTTP_400_BAD_REQUEST
            )
        
        data['paymentedetails'] = payment_obj.pk
        data['lead'] = lead_obj.pk
        serializer = self.serializer_class(data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(
                    response_data(False, "KYC created successfully", serializer.data),
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            return Response(
                response_data(True, e, serializer.errors),
                status=status.HTTP_400_BAD_REQUEST,
            )
