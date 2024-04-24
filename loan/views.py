from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import LoanSerializer
from .models import Loan
from utils import response_data
from applicants.models import Applicants

class LoanAPIView(APIView):
    serializer_class = LoanSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Loan.objects.all()

    def get(self, request):
        try:
            loan_id = request.query_params.get('loan_id', None)
            
            if loan_id:
                if self.queryset.filter(loan_id=loan_id).exists():
                    loan_obj = self.queryset.get(loan_id=loan_id)
                    serializer = self.serializer_class(loan_obj)
                    return Response(
                        response_data(False, "Loan found", serializer.data),
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        response_data(True, "Loan not found."),
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                loans = self.queryset.all()
                serializer = self.serializer_class(loans, many=True)
                return Response(
                    response_data(False, "Loans found", serializer.data),
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            return Response(
                response_data(True, e),
                status=status.HTTP_400_BAD_REQUEST
            )

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

        serializer = self.serializer_class(data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(
                    response_data(False, "Loan created successfully", serializer.data),
                    status=status.HTTP_201_CREATED,
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

    def put(self, request, loan_id):
        try:
            loan_obj = self.queryset.get(loan_id=loan_id)
        except Loan.DoesNotExist:
            return Response(
                response_data(True, "Loan not found."),
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(loan_obj, data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(
                    response_data(False, "Loan updated successfully", serializer.data),
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

    def delete(self, request, loan_id):
        try:
            loan_obj = self.queryset.get(loan_id=loan_id)
        except Loan.DoesNotExist:
            return Response(
                response_data(True, "Loan not found."),
                status=status.HTTP_404_NOT_FOUND
            )

        loan_obj.delete()
        return Response(
            response_data(False, "Loan deleted successfully"),
            status=status.HTTP_204_NO_CONTENT,
        )
