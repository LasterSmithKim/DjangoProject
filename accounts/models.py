from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    # 一对一关联到内置的 User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 新增字段：头像
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    # 新增字段：个人简介
    bio = models.TextField(max_length=500, blank=True)
    # 新增字段：手机号
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username} 的档案"
