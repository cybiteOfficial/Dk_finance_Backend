from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils import response_data, save_comment
from user_auth.models import User
from .models import Leads
from .serializers import LeadsSerializer
from error_logs.models import UserLog

from rest_framework import permissions
from kyc.models import KYCDetails

class LeadView(APIView):
    serializer_class = LeadsSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Leads.objects.all()

    def get_lead(self, lead_id):
        try:
            return self.queryset.get(lead_id=lead_id)
        except Leads.DoesNotExist:
            return None
    
    def post(self, request):
        if User.objects.filter(email=request.user.email).exists():
            if User.objects.get(email=request.user.email).user_type != 'ro':
                return Response(
                    response_data(True, "User not have permission"),
                    status.HTTP_400_BAD_REQUEST
                )
            user = User.objects.get(email=request.user.email, user_type = 'ro')

        else:
            return Response(
                response_data(True, "User not found"), status.HTTP_400_BAD_REQUEST
            )
        
        data = request.data.copy()
        data['mobile_number'] = '+91' + data['mobile_number']
        new_data = {}
        for field in ["gender", "first_name", "last_name"]:
            if request.data.get(field):
                new_data[field] = (
                    request.data[field].lower()
                    if field == "gender"
                    else request.data[field].capitalize()
                )
        data['assigned_to'] = user.pk
        comment = save_comment(data.get('comment'))
        if comment:
            data['comment'] = comment.pk
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            data = serializer.save()
            KYCDetails.objects.create(lead_id=data, kyc_verified=False, kyc_document_verified=False)
            
            # Logs
            logged_user = User.objects.get(username=request.user.username)
            api = 'POST api/v1/leads'
            details = f'created lead id {data}'
            UserLog.objects.create(
                user=logged_user, 
                api=api,
                details=details,
            )
            
            return Response(
                response_data(False, "Lead created successfully", serializer.data),
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                response_data(True, "Something went wrong", serializer.errors),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request):
        try:
            leads = self.queryset.filter(assigned_to__email = request.user.email).order_by('-lead_id')
            if leads:
                serializer = self.serializer_class(leads, many=True)
                
                # Logs
                logged_user = User.objects.get(username=request.user.username)
                api = 'GET api/v1/leads'
                details = f'viewed leads of user({request.user.username})'
                UserLog.objects.create(
                    user=logged_user, 
                    api=api,
                    details=details,
                )
                    
                return Response(
                    response_data(False, "User found.", serializer.data), status.HTTP_200_OK
                )
            else:
                return Response(
                response_data(True, "Does not contains any lead for this user."), status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                response_data(True, "Something went wrong"), status.HTTP_400_BAD_REQUEST
            )
        
    def put(self, request):
        try:
            lead_id = request.query_params.get('lead_id')
            lead_obj = self.get_lead(lead_id)

            if lead_obj:
                serializer = self.serializer_class(lead_obj, request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    
                    # Logs
                    logged_user = User.objects.get(username=request.user.username)
                    api = 'PUT api/v1/leads'
                    details = f'updated lead {lead_id}'
                    UserLog.objects.create(
                        user=logged_user, 
                        api=api,
                        details=details,
                    )
                    
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
                        response_data(True, "Lead Object Not Found."),
                        status=status.HTTP_200_OK,
                    )
        except Exception as e:
            return Response(
                response_data(True, "Something went wrong.", e),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request):
        lead_id = request.query_params.get('lead_id')
        lead_obj = self.get_lead(lead_id)
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
        

# for website only 

class LeadViewForWeb(APIView):
    serializer_class = LeadsSerializer
    queryset = Leads.objects.all()

    authentication_classes = [] 
    permission_classes = [permissions.AllowAny] 

    def post(self, request):
        data = request.data.copy()
        data['mobile_number'] = '+91' + data['mobile_number']
        new_data = {}
        for field in ["gender", "first_name", "last_name"]:
            if request.data.get(field):
                new_data[field] = (
                    request.data[field].lower()
                    if field == "gender"
                    else request.data[field].capitalize()
                )
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                response_data(False, "Lead created successfully"),
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                response_data(True, "Something went wrong", serializer.errors),
                status=status.HTTP_400_BAD_REQUEST,
            )