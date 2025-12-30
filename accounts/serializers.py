from rest_framework import serializers
from django.contrib.auth.models import User
from products.models import Category
from django.contrib.auth.hashers import make_password
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'phone']


class RegisterSerializer(serializers.ModelSerializer):
    # 密码设置为只写，不在返回结果中显示
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True)
    # 这里的 profile 不再是 read_only=True，而是要接收数据
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'profile']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已被占用。")
        return value

    def create(self, validated_data):
        # 1. 弹出 profile 数据（如果没有传，默认为空字典）
        profile_data = validated_data.pop('profile', {})
        # 核心：使用 create_user 自动处理密码加密
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        # 自动化逻辑：新用户注册后，自动加入 ID 为 4 的“公共分类”
        try:
            public_category = Category.objects.get(id=4)
            # 这行代码会在你的 products_category_allowed_users 表里增加一条记录
            public_category.allowed_users.add(user)
        except Category.DoesNotExist:
            pass  # 如果不存在 ID 为 1 的分类，则跳过
        # 3. 更新由信号自动创建的 Profile
        # 因为是 OneToOneField，我们可以直接通过 user.profile 访问它
        if profile_data:
            profile = user.profile  # 获取信号刚创建好的那个对象
            profile.bio = profile_data.get('bio', profile.bio)
            profile.phone = profile_data.get('phone', profile.phone)
            # 如果有头像上传，也可以在这里处理
            if 'avatar' in profile_data:
                profile.avatar = profile_data['avatar']
            profile.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    # 嵌套显示档案信息，注意这里的 profile 名字要和 User 模型里的 related_name 一致
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']
