from rest_framework import serializers
from django.contrib.auth.models import User
from products.models import Category
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
    # 密码设置为只写，不在返回结果中显示
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已被占用。")
        return value

    def create(self, validated_data):
        # 核心：使用 create_user 自动处理密码加密
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        # 自动化逻辑：新用户注册后，自动加入 ID 为 1 的“公共分类”
        try:
            public_category = Category.objects.get(id=4)
            # 这行代码会在你的 products_category_allowed_users 表里增加一条记录
            public_category.allowed_users.add(user)
        except Category.DoesNotExist:
            pass  # 如果不存在 ID 为 1 的分类，则跳过
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']