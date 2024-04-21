from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import get_user_model, authenticate

from .serializers import SignUpSerializer, SignInSerializer, UserSerializer, BankDetailsSerializer
from utils import response_data, OauthGetToken

class SignUpView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer
    user = get_user_model()

    def post(self, request):
        for field in ["gender", "first_name", "last_name"]:
            if request.data.get(field):
                request.data[field] = (
                    request.data[field].lower()
                    if field == "gender"
                    else request.data[field].capitalize()
                )

        serializer = self.serializer_class(data=request.data)
        
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
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )
            if user:
                response, status_code = OauthGetToken(data.get('email'), data.get('password'))
                if status_code ==  200:
                    return Response(
                        response_data(False, "Successfully login.", response.json()),
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
            current_user = request.user
            serializer = self.serializer_class(current_user)
            return Response(
                response_data(False, "User found.", serializer.data), status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                response_data(True, "Something went wrong"), status.HTTP_400_BAD_REQUEST
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
        pk = request.query_params.get("pk")
        user_obj = self.get_user(pk)
        if user_obj :
            if not request.user.is_superuser:
                return Response(
                    response_data(True, "Permission denied for the user."),
                    status.HTTP_401_UNAUTHORIZED,
                )
            user_obj.delete()
            return Response(response_data(False, "User Deleted."), status.HTTP_200_OK)
        else:
            return Response(response_data(True, "User not found."), status.HTTP_404_NOT_FOUND)


class BankDetailsCreateAPIView(APIView):
    def post(self, request):
        serializer = BankDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_data(False, "Bank Added Successfully!"), status.HTTP_200_OK)
        return Response(response_data(False, "Fail to add bank details"), status.HTTP_200_OK)