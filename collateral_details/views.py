from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import CollateralDetails
from .serializers import CollateralDetailsSerializer
from applicants.models import Applicants
from utils import response_data, save_comment

class CollateralDetailsAPIView(APIView):
    serializer_class = CollateralDetailsSerializer
    permission_classes = (IsAuthenticated,)
    queryset = CollateralDetails.objects.all()

    def get_collateral_detail(self, pk):
        try:
            return self.queryset.get(collateral_id=pk)
        except CollateralDetails.DoesNotExist:
            return None
    
    def post(self, request):

        data = request.data.copy()
        application_id = request.query_params.get('application_id')
        if Applicants.objects.filter(application_id = application_id).exists():
            applicant = Applicants.objects.get(application_id = application_id)
            data['applicant'] = applicant.pk
        else:
            return Response(
                response_data(True, "Applicant not found"), status.HTTP_400_BAD_REQUEST
            )
        comment = save_comment(data.get('comment'))
        if comment:
            data['comment'] = comment.pk
        serializer = self.serializer_class(data=request.data)
        
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(
                    response_data(False, "Collateral detail created successfully", serializer.data),
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    response_data(True, "Something went wrong", serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                response_data(True, e, serializer.errors),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request):
        try:
            collateral_id = request.query_params.get('collateral_id', None)
            if collateral_id:
                if self.queryset.filter(collateral_id=collateral_id).exists():
                    collateral_obj = self.queryset.get(collateral_id=collateral_id)
                    serializer = self.serializer_class(collateral_obj)
                    return Response(
                        response_data(False, "collateral details found", serializer.data),
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        response_data(True, "Loan not found."),
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                return Response(
                    response_data(True, "Collateral detail not found"),
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            return Response(
                response_data(True, e),
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, collateral_id):
        collateral_detail = self.get_collateral_detail(collateral_id)
        if collateral_detail:
            serializer = self.serializer_class(collateral_detail, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    response_data(False, "Collateral detail updated successfully", serializer.data),
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    response_data(True, "Something went wrong", serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                response_data(True, "Collateral detail not found"),
                status=status.HTTP_404_NOT_FOUND,
            )

    def delete(self, request, collateral_id):
        collateral_detail = self.get_collateral_detail(collateral_id)
        if collateral_detail:
            collateral_detail.delete()
            return Response(response_data(False, "Collateral detail deleted."), status.HTTP_200_OK)
        else:
            return Response(response_data(True, "Collateral detail not found."), status.HTTP_404_NOT_FOUND)
