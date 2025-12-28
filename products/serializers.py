from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    # 方式 A：直接显示分类名称（只读）
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'created_at', 'image', 'category', 'category_name']

