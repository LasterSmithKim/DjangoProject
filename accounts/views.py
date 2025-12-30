from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .serializers import RegisterSerializer,UserSerializer,ProfileSerializer
from rest_framework.parsers import MultiPartParser, FormParser

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

class ProfileUpdateView(generics.UpdateAPIView):
    """
    允许登录用户修改自己的档案（头像、简介等）
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] # 支持头像上传

    def get_object(self):
        # 核心逻辑：这个接口不需要在 URL 里传 ID，直接返回当前登录用户的 profile
        return self.request.user.profile