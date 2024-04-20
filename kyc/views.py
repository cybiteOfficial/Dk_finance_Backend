from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils import response_data
from leads.models import Leads
from .models import KYCDetails
from .serializers import KycDetailsSerializer

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
        lead_id = request.data.get('lead_id')
        if Leads.objects.filter(lead_id=lead_id).exists():  
            lead_obj = Leads.objects.get(lead_id=lead_id)
        else:
            return Response(
                response_data(True, "Lead not found"), status.HTTP_400_BAD_REQUEST
            )
        
        data = request.data.copy()
        for field in ["first_name", "last_name"]:
            if request.data.get(field):
                data[field] = request.data[field].capitalize()
                
        data['lead'] = lead_obj.pk
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
        import pdb;pdb.set_trace()
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
        lead_id = request.query_params.get('lead_id')
        lead_obj = self.get_kyc_object(lead_id)
        if lead_obj :
            if not request.user.is_superuser:
                return Response(
                    response_data(True, "Permission denied for the user."),
                    status.HTTP_401_UNAUTHORIZED,
                )
            lead_obj.delete()
            return Response(response_data(False, "Lead Deleted."), status.HTTP_200_OK)
        else:
            return Response(response_data(True, "Lead object not found."), status.HTTP_200_OK)
