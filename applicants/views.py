from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import ApplicantsSerializer
from .models import Applicants
from leads.models import Leads
from phonepay.models import Payment

from utils import response_data, save_comment, generate_OrderID
from pagination import CommonPagination

class ApplicantAPIView(APIView):
    serializer_class = ApplicantsSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Applicants.objects.all()
    pagination_class = CommonPagination

    def get(self, request):
        try:
            application_id = request.query_params.get('application_id', None)
            
            if application_id:
                if self.queryset.filter(application_id = application_id).exists():
                    applicant_objs = self.queryset.filter(application_id = application_id)
                else:
                    return Response(
                    response_data(True, "Not found any Applicant."), status.HTTP_200_OK
                )
            else:
                applicant_objs = self.queryset.all()
            
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

        comment = save_comment(data['comment'])
        if comment:
            data['comment'] = comment.pk
        
        serializer = self.serializer_class(data=data)
        try:
            if serializer.is_valid():
                serializer.save()
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
        import pdb;pdb.set_trace()
        order_id = generate_OrderID()
        if order_id:
            Payment.objects.create(order_id=order_id)
            paymt_obj = Payment.objects.get(order_id=order_id)
        Applicants.objects.create(paymentedetails=paymt_obj)
        applicant = Applicants.objects.get(paymentedetails=paymt_obj)
        serializer = self.serializer_class(applicant)
        return Response(
            response_data(False, "Applicant created successfully", serializer.data),
            status=status.HTTP_200_OK,
        )