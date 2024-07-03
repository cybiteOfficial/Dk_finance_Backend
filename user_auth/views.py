from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import get_user_model, authenticate

from .serializers import SignUpSerializer, SignInSerializer, UserSerializer, BankDetailsSerializer
from utils import response_data, OauthGetToken, save_comment, generate_empID
from .models import User, BankDetails

class SignUpView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer
    user = get_user_model()

    def post(self, request):
        data = request.data.copy()

        for field in ["gender", "first_name", "last_name"]:
            if data.get(field):
                data[field] = (
                    data[field].lower()
                    if field == "gender"
                    else data[field].capitalize()
                )
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():   
            serializer.save()
            return Response(
                response_data(False, "User Created.", serializer.data),
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                response_data(True, "Something went wrong", serializer.errors),
                status=status.HTTP_400_BAD_REQUEST,
            )

class SignInView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer
    user = get_user_model()

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )
            if user:
                response, status_code = OauthGetToken(data.get('username'), data.get('password'))
                res = response.json()
                if status_code ==  200:
                    res['user_type'] = user.user_type
                    return Response(
                        response_data(False, "Successfully login.", res),
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        response_data(True, "Invalid credentials", response.text),
                        status=status.HTTP_401_UNAUTHORIZED,
                )
            else:
                return Response(
                    response_data(True, "Invalid credentials"),
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(
                response_data(True, "Something went wrong", serializer.errors),
                status=status.HTTP_400_BAD_REQUEST,
            )

class UserView(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    user = get_user_model()

    def get_user(self, pk):
        try:
            return self.user.objects.get(pk=pk)
        except self.user.DoesNotExist:
            return None

    def get(self, request):
        try:
            user = request.user
            bank_branch = user.bank_branch
            
            if user.user_type == 'ro' or user.user_type == 'do' or user.user_type == 'technicalofficer':
                queryset = User.objects.filter(bank_branch=bank_branch).order_by('-created_at')
                
            else:
                queryset = User.objects.all()
                
            serializer = self.serializer_class(queryset, many=True)
            
            return Response(
                response_data(False, serializer.data),
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                response_data(True, "Something went wrong", str(e)), status.HTTP_400_BAD_REQUEST
            )
        
    def put(self, request):
        try:
            user_obj = self.get_user(request.user.pk)
            if user_obj:
                new_data = {}
                for field in ["gender", "first_name", "last_name"]:
                    if request.data.get(field):
                        new_data[field] = (
                            request.data[field].lower()
                            if field == "gender"
                            else request.data[field].capitalize()
                        )
                serializer = self.serializer_class(user_obj , new_data, partial=True)
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
                        response_data(True, "Unknown User"),
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
        except Exception as e:
            return Response(
                response_data(True, "Something went wrong.", e),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request):
        username = request.query_params.get('username')
        try:
            user = User.objects.get(username=username, is_active=True)
            
            if user:
                user.is_active = False
                user.save()
                return Response(
                    response_data(False, "User deleted successfully"),
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    response_data(True, "User not found"),
                    status=status.HTTP_404_NOT_FOUND,
                )
        
        except Exception as e:
            return Response(
                response_data(True, str(e)),
                status=status.HTTP_400_BAD_REQUEST,
            )
            

class BankBranchView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        data = request.data 
        
        comment = save_comment(data.get('comment'))
        if comment:
            data['comment'] = comment.pk
        
        serializer = BankDetailsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                response_data(False, "Created Successfully.", serializer.data),
                status=status.HTTP_201_CREATED,
            )
            
        return Response(
                response_data(True, serializer.errors),
                status=status.HTTP_400_BAD_REQUEST,
            )
        
    def get(self, request):
        queryset = BankDetails.objects.all()
        serializer = BankDetailsSerializer(queryset, many=True)
        return Response(
            response_data(False, "Fetched Successfully.", serializer.data),
            status=status.HTTP_200_OK,
        )