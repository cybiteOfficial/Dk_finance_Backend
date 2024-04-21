from rest_framework import generics
from rest_framework.response import Response
from .models import CustomerDetails
from .serializers import CustomerDetailsSerializer

from applicants.models import Applicants

from utils import response_data
from rest_framework import status

# Create your views here.
class CustomerDetailsAPIView(generics.ListCreateAPIView):
    queryset = CustomerDetails.objects.all()
    serializer_class = CustomerDetailsSerializer

    def get_customer(self, customer_id):
        try:
            return self.queryset.get(cif_id=customer_id)
        except CustomerDetails.DoesNotExist:
            return None
        
    def get(self, request):
        try:
            customer = self.queryset.filter(cif_id = request.data.customer_id)
            if customer:
                serializer = self.serializer_class(customer, many=True)
                return Response(
                    response_data(False, "Customer found.", serializer.data), status.HTTP_200_OK
                )
            else:
                return Response(
                response_data(True, "Customer details does not exits."), status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                response_data(True, "Something went wrong"), status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        if Applicants.objects.filter(application_id = request.data.application_id).exists():
            applicant = Applicants.objects.get(application_id = request.data.application_id)
        else:
            return Response(
                response_data(True, "Applicant not found"), status.HTTP_400_BAD_REQUEST
            )
        data = request.data.copy()

        data['applicant'] = applicant.pk
        serializer = self.serializer_class(data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(
                    response_data(False, "Customer created successfully", serializer.data),
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            return Response(
                response_data(True, e, serializer.errors),
                status=status.HTTP_400_BAD_REQUEST,
            )
