from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import ApplicantsSerializer
from .models import Applicants, AuditTrail
from leads.models import Leads
from phonepay.models import Payment
from user_auth.models import User

from utils import response_data, save_comment, generate_OrderID, generate_applicationID
from pagination import CommonPagination
from choices import Choices
from django.db import transaction
from kyc.models import KYCDetails, DocumentsUpload
from error_logs.models import UserLog


class ApplicantAPIView(APIView):
    serializer_class = ApplicantsSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Applicants.objects.filter(is_active=True).order_by('-updated_at')
    pagination_class = CommonPagination

    def get(self, request):
        try:
            application_id = request.query_params.get('application_id', None)
            user_email = request.user.email  
            
            user = User.objects.filter(email = user_email)
            
            # Logs
            logged_user = User.objects.get(username = request.user.username)
            api = 'GET api/v1/applicants'
            details = 'Viewed applicants'
            UserLog.objects.create(user=logged_user, api=api, details=details)

            for details in user:
                user_type = details.user_type
            
            if application_id:
                if self.queryset.filter(application_id = application_id).exists():
                    applicant_objs = self.queryset.filter(application_id = application_id)
                else:
                    return Response(
                    response_data(True, "Not found any Applicant."), status.HTTP_200_OK
                )
        
            elif user_type == 'md' or user_type == 'cluster':
                applicant_objs = self.queryset.all()

            else:
                user = User.objects.filter(email = user_email)
                user_uuid = user[0].pk
                applicant_objs = self.queryset.filter(created_by = user_uuid)

                
            paginator = self.pagination_class()
            paginated_res = paginator.paginate_queryset(applicant_objs, request)
        
            serializer = self.serializer_class(paginated_res, many= True)
            
            return  paginator.get_paginated_response(serializer.data)

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
            if payment_obj.status.lower() != "done":
                return Response(
                    response_data(True, "Payment is Pending"), status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                response_data(True, "Payment is not Done yet"), status.HTTP_400_BAD_REQUEST
            )
        
        data['paymentedetails'] = payment_obj.pk
        data['lead'] = lead_obj.pk

        comment = save_comment(data.get('comment'))
        if comment:
            data['comment'] = comment.pk
        
        serializer = self.serializer_class(data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                
                logged_user = User.objects.get(username = request.user.username)
                api = 'POST api/v1/applicants'
                details = 'Created applicant'
                UserLog.objects.create(user=logged_user, api=api, details=details)
                
                return Response(
                    response_data(False, "Applicant created successfully", serializer.data),
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

class CreateAppForPaymentReference(APIView):
    serializer_class = ApplicantsSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Applicants.objects.all()
    pagination_class = CommonPagination

    def post(self, request):
        username = request.user.username
        order_id = generate_OrderID()
        application_id = generate_applicationID()
        # kyc_id = request.data.get('kyc_id')
        lead_id = request.query_params.get('lead_id')

        created_by = User.objects.get(username = username)
        
        if order_id:
            Payment.objects.create(order_id=order_id)
            paymt_obj = Payment.objects.get(order_id=order_id)
        if lead_id:
            lead_obj = Leads.objects.get(lead_id=lead_id)
            if lead_obj == None:
                return Response(
                    response_data(True, "Lead id not found"),
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                response_data(True, "Lead id is required"),
                status=status.HTTP_400_BAD_REQUEST,
            )

        Applicants.objects.create(application_id=application_id, paymentedetails=paymt_obj, lead = lead_obj, created_by=created_by)
        applicant = Applicants.objects.get(paymentedetails=paymt_obj)
        # DocumentsUpload.objects.filter(kyc__uuid = kyc_id).update(application_id = applicant)
        
        # logs
        logged_user = User.objects.get(username = request.user.username)
        api = 'POST api/v1/create_app_id'
        details = f'Created applicant: {applicant.application_id}'
        UserLog.objects.create(user=logged_user, api=api, details=details)
            
        serializer = self.serializer_class(applicant)
        return Response(
            response_data(False, "Applicant created successfully", serializer.data),
            status=status.HTTP_200_OK,
        )

class UpdateApplicationStatus(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            status_list = Choices.FORWARD_STATUS_BINDING
            app_ids = eval(request.data.get("applications_ids"))
            event = Applicants.objects.filter(application_id__in=app_ids).values('application_id', 'status')
            data = {}
            for item in event:
                if data.get(item["status"]):
                    data.get(item["status"]).append(item["application_id"])
                else:
                    data[item["status"]]= [item["application_id"]]
            for key, value in data.items():
                new_status = status_list.get(key)
                applicant_to_update = Applicants.objects.filter(application_id__in=app_ids)
                applicant_to_update.update(status= new_status)

                with transaction.atomic():
                    for applicant in applicant_to_update:
                        audit_trail = AuditTrail.objects.create(application_id=applicant, current_status=key, updated_status=new_status, updated_by=request.user)
                        created_at = audit_trail.created_at
                        Applicants.objects.filter(application_id = applicant).update(updated_at = created_at, status = new_status)
                        
                        # logs
                        logged_user = User.objects.get(username = request.user.username)
                        api = 'POST api/v1/update_status'
                        details = f'Updated status of applicant: {applicant.application_id} from {key} to {new_status}'
                        UserLog.objects.create(user=logged_user, api=api, details=details)

                return Response(response_data(False, "Status updated successfully"), status=status.HTTP_200_OK)
        except:
            return Response(response_data(True, "status not updated"), status=status.HTTP_400_BAD_REQUEST)