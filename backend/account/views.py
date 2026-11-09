from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from .models import *
from .serializers import *

class LoginView(APIView):
    permission_classes = [ AllowAny ]

    def post(self, request: Request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data.get('username'),
            password=serializer.validated_data.get('password'),
        )
        if not user:
            return Response({'detail': '로그인 실패'}, status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response({'detail': '로그인 성공'}, status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [ IsAuthenticated ]

    def post(self, request: Request):
        logout(request)
        return Response({'detail': '로그아웃 성공'}, status.HTTP_200_OK)

class MyProfileView(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request: Request):
        serializer = ProfileSerializer(request.profile)
        return Response(serializer.data, status.HTTP_200_OK)