from django.contrib import admin

# Register your models here.
# products/admin.py

from django.contrib import admin
from .models import Product,Category,ProductImage  # 从你刚刚创建的 models.py 中导入 Product


# 1. 定义内联管理器（让图片出现在商品编辑页底部）
class ProductImageInline(admin.TabularInline): # TabularInline 是横向排列，更省空间
    model = ProductImage
    extra = 1  # 默认显示 1 个空白上传框
    fields = ['image']

# 或者使用更专业的装饰器方式（推荐，因为可以配置显示哪些列）
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'show_main_image') # 在列表页显示分类列
    # 允许在列表页直接编辑的字段
    list_editable = ['price', 'category']

    # 过滤器：在侧边栏增加分类筛选
    list_filter = ['category', 'created_at']

    # 搜索框：支持按名称搜索
    search_fields = ['name']

    # ⚠️ 关键：将多图管理内联进来
    inlines = [ProductImageInline]

    # 自定义方法：在列表页显示主图的缩略图（5.0 实用技巧）
    def show_main_image(self, obj):
        if obj.image:
            from django.utils.html import format_html
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />', obj.image.url)
        return "无主图"

    show_main_image.short_description = "商品主图"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # 针对多对多字段，提供一个好用的横向穿梭框界面
    filter_horizontal = ('allowed_users',)