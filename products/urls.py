 #products/urls.py

from django.urls import path,include
from . import views  # 导入你的视图文件
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet,CategoryViewSet

app_name = 'products'  # <--- 必须加这一行，且值要与 namespace 一致

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'', ProductViewSet) # 注册路径为 products/


urlpatterns = [
    # 当路径为空（即 /products/ 时），调用 views.product_list 函数
    # path('', views.product_list, name='product-list'),
    path('api/', include(router.urls)),


    path('index/', views.ProductListView.as_view(), name='product_list'),
    #path('index/', views.product_index, name='product_list'),

    # 新增：访问 /products/create/ 时调用 product_create 视图
    path('add/', views.product_create, name='product_add'),  # 确保有这一行
    path('create/', views.product_create, name='product-create'),

    # 新增：<int:pk> 表示匹配一个整数，并将其作为参数 pk 传给视图
    # pk 代表 Primary Key (主键)
    path('<int:pk>/', views.product_detail, name='product-detail'),

    path('<int:pk>/edit/', views.product_update, name='product-update'),
    path('<int:pk>/delete/', views.product_delete, name='product-delete'),
]