from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .serializers import RegisterSerializer,UserSerializer

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny] # 允许任何人注册
    serializer_class = RegisterSerializer

class UserMeView(APIView):
    permission_classes = [IsAuthenticated] # 必须登录才能看自己

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)