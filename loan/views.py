from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import LoanSerializer
from .models import Loan
from utils import response_data, save_comment
from applicants.models import Applicants
from user_auth.serializers import CommentSerializer
from user_auth.models import User
from error_logs.models import UserLog

class LoanAPIView(APIView):
    serializer_class = LoanSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Loan.objects.all()

    def get(self, request):
        try:
            loan_id = request.query_params.get('loan_id', None)
            application_id = request.query_params.get('application_id', None)
            if loan_id:
                if self.queryset.filter(loan_id=loan_id).exists():
                    loan_obj = self.queryset.get(loan_id=loan_id)
                    serializer = self.serializer_class(loan_obj)
                    
                    # Logs
                    logged_user = User.objects.get(username=request.user.username)
                    api = 'GET api/v1/loan_details'
                    details = f'viewed loan details of {loan_id}'
                    UserLog.objects.create(user=logged_user, api=api, details=details)
                    
                    return Response(
                        response_data(False, "Loan found", serializer.data),
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        response_data(True, "Loan not found."),
                        status=status.HTTP_404_NOT_FOUND
                    )
            elif application_id:
                loans_details = Loan.objects.filter(applicant__application_id = application_id)
                serializer = self.serializer_class(loans_details, many=True)
                
                # Logs
                logged_user = User.objects.get(username=request.user.username)
                api = 'GET api/v1/loan_details'
                details = f'viewed loan details of {application_id}'
                applicant = Applicants.objects.get(application_id=application_id)
                UserLog.objects.create(
                    user=logged_user,
                    api=api,
                    details=details,
                    applicant_id=applicant.pk
                )
                
                return Response(
                    response_data(False, "Loan found", serializer.data),
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    response_data(True, "App id or loan id not provided"),
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            return Response(
                response_data(True, str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        data = request.data.copy()
        loan_id = data.get('loan_id')

        application_id = data.get('applicant_id')
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
        
        if loan_id:

            if Loan.objects.filter(loan_id=loan_id).exists():
                loan_obj = Loan.objects.get(loan_id=loan_id)
                serializer = self.serializer_class(loan_obj, data=data)
                try:
                    if serializer.is_valid():
                        serializer.save()
                        
                        # Logs
                        logged_user = User.objects.get(username=request.user.username)
                        api = 'POST api/v1/loan_details'
                        details = f'updated loan details of {application_id}'
                        applicant = Applicants.objects.get(application_id=application_id)
                        UserLog.objects.create(
                            user=logged_user,
                            api=api,
                            details=details,
                            applicant_id=applicant.pk
                        )
                        
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
        else:
            serializer = self.serializer_class(data=data)
            try:
                if serializer.is_valid():
                    serializer.save()
                    
                    # Logs
                    logged_user = User.objects.get(username=request.user.username)
                    api = 'POST api/v1/loan_details'
                    details = f'created loan details of {application_id}'
                    applicant = Applicants.objects.get(application_id=application_id)
                    UserLog.objects.create(
                        user=logged_user,
                        api=api,
                        details=details,
                        applicant_id=applicant.pk
                    )

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
