from rest_framework import serializers
from .models import Product,Category



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name','detail'] # 只包含 ID 和名称
class ProductSerializer(serializers.ModelSerializer):
    # 方式 A：直接显示分类名称（只读）
    category_name = serializers.ReadOnlyField(source='category.name')

    # 方式 B：使用嵌套序列化器替换 category ID 字段
    # category = CategorySerializer()
    # 方式 B：将嵌套序列化器设为 read_only=True
    # 这样“看”的时候有详细信息，但“写”的时候它会跳过这个字段，去寻找模型原有的 category (ID)
    category_detail = CategorySerializer(source='category', read_only=True)

    # 显式声明 image 为文件字段。注意：不要加 read_only=True
    # image = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'created_at', 'image', 'category', 'category_name', 'category_detail']

