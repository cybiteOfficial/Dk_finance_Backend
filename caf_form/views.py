from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import CafDetails
from .serializers import CafSerializer
from applicants.models import Applicants
from utils import response_data, save_comment
from customer.models import CustomerDetails

class CafFomAPIView(APIView):
    serializer_class = CafSerializer
    permission_classes = (IsAuthenticated,)
    queryset = CafDetails.objects.all()

    def get_caf_detail(self, pk):
        try:
            return self.queryset.get(caf_id=pk)
        except CafDetails.DoesNotExist:
            return None
    
    def post(self, request):
        data = request.data.copy()
        caf_id = data.get('caf_id')
        if caf_id and CafDetails.objects.filter(caf_id=caf_id).exists():
            caf_obj = CafDetails.objects.get(caf_id=caf_id)
            serializer = self.serializer_class(caf_obj, data=data)
        else:
            application_id = data.get('applicant_id')
            customer_id = data.get('customer_id')
            if Applicants.objects.filter(application_id=application_id).exists():
                applicant = Applicants.objects.get(application_id=application_id)
                data['applicant'] = applicant.pk
            else:
                return Response(response_data(True, "Applicant not found"), status=status.HTTP_400_BAD_REQUEST)

            if CustomerDetails.objects.filter(cif_id=customer_id, applicant__application_id = application_id).exists():
                customer_obj = CustomerDetails.objects.get(cif_id=customer_id, applicant__application_id = application_id)
                data['customer'] = customer_obj.pk
            else:
                return Response(response_data(True, "customer not found"), status=status.HTTP_400_BAD_REQUEST)

            comment = save_comment(data.get('comment'))
            if comment:
                data['comment'] = comment.pk

            serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_data(False, "caf created successfully", serializer.data), status=status.HTTP_201_CREATED)
        else:
            return Response(response_data(True, "Something went wrong", serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            caf_id = request.query_params.get('caf_id')
            if caf_id:
                if self.queryset.filter(caf_id=caf_id).exists():
                    caf_obj = self.queryset.get(caf_id=caf_id)
                    serializer = self.serializer_class(caf_obj)
                    return Response(response_data(False, "Collateral details found", serializer.data), status=status.HTTP_200_OK)
                else:
                    return Response(response_data(True, "Collateral not found"), status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(response_data(True, "CAF ID not provided"), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(response_data(True, str(e)), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, caf_id):
        caf_details = self.get_caf_detail(caf_id)
        if caf_details:
            caf_details.delete()
            return Response(response_data(False, "CAF detail deleted"), status=status.HTTP_200_OK)
        else:
            return Response(response_data(True, "CAF detail not found"), status=status.HTTP_404_NOT_FOUND)
