from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Customer_Caf
from .serializers import Customer_CafSerializer
from applicants.models import Applicants
from utils import response_data, save_comment

class Customer_CafAPIView(APIView):
    serializer_class = Customer_CafSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Customer_Caf.objects.order_by('-created_at')

    def get_caf_detail(self, pk):
        try:
            return self.queryset.get(caf_id=pk)
        except Customer_Caf.DoesNotExist:
            return None
    
    def post(self, request):
        data = request.data.copy()
        caf_id = data.get('caf_id')

        if caf_id and Customer_Caf.objects.filter(caf_id=caf_id).exists():
            caf_obj = Customer_Caf.objects.get(caf_id=caf_id)
            serializer = self.serializer_class(caf_obj, data=data)
        else:
            application_id = data.get('applicant_id')
            if Applicants.objects.filter(application_id=application_id).exists():
                applicant = Applicants.objects.get(application_id=application_id)
                data['applicant'] = applicant.pk
            else:
                return Response(response_data(True, "Applicant not found"), status=status.HTTP_400_BAD_REQUEST)

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
            application_id = request.query_params.get('application_id')
            if caf_id:
                if self.queryset.filter(caf_id=caf_id).exists():
                    caf_obj = self.queryset.get(caf_id=caf_id)
                else:
                    return Response(response_data(True, "Collateral not found"), status=status.HTTP_404_NOT_FOUND)
            elif application_id:
                if self.queryset.filter(applicant__application_id=application_id).exists():
                    caf_obj = self.queryset.get(applicant__application_id=application_id)
                else:
                    return Response(response_data(True, "Collateral not found"), status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(response_data(True, "CAF ID not provided"), status=status.HTTP_400_BAD_REQUEST)
            
            serializer = self.serializer_class(caf_obj)
            return Response(response_data(False, "Collateral details found", serializer.data), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(response_data(True, str(e)), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, caf_id):
        caf_details = self.get_caf_detail(caf_id)
        if caf_details:
            serializer = self.serializer_class(caf_details, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(response_data(False, "CAF detail updated successfully", serializer.data), status=status.HTTP_200_OK)
            else:
                return Response(response_data(True, "Something went wrong", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response_data(True, "CAF detail not found"), status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, caf_id):
        caf_details = self.get_caf_detail(caf_id)
        if caf_details:
            caf_details.delete()
            return Response(response_data(False, "CAF detail deleted"), status=status.HTTP_200_OK)
        else:
            return Response(response_data(True, "CAF detail not found"), status=status.HTTP_404_NOT_FOUND)
