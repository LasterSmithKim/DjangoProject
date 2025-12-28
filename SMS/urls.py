"""
URL configuration for SMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
# 导入 simplejwt 的视图
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # 这一行会开启：/accounts/login/, /accounts/logout/ 等路由
    path('accounts/', include('django.contrib.auth.urls')),
    # path('api/products/', include('products.urls',namespace='apiproducts')), # 将 products 的 API 挂在 api/products/ 下
    path('products/', include('products.urls', namespace='products')),

# 添加 JWT 认证的 URL 路由
    # 使用这个端点获取 access 和 refresh token（登录）
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # 使用这个端点刷新 access token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

