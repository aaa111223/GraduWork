from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from apps.users.models import User


class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_data = UserSerializer(user).data
            return Response({
                'message': 'Registration successful',
                'user': user_data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            # Get user data
            user_data = UserSerializer(user).data

            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': user_data,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        return Response({'message': 'Logout endpoint'}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    def post(self, request):
        return Response({'message': 'Change password endpoint'}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    def post(self, request):
        return Response({'message': 'Reset password endpoint'}, status=status.HTTP_200_OK)


class SendVerificationCodeView(APIView):
    def post(self, request):
        return Response({'message': 'Send verification code endpoint'}, status=status.HTTP_200_OK)


class VerifyCodeView(APIView):
    def post(self, request):
        return Response({'message': 'Verify code endpoint'}, status=status.HTTP_200_OK)


class LoginLogListView(APIView):
    def get(self, request):
        return Response({'message': 'Login logs endpoint'}, status=status.HTTP_200_OK)
