# products/models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="分类名")
    detail = models.CharField(max_length=100,verbose_name="分类详情")
    # 建立分类与用户的多对多关系：哪些用户能看这个分类
    allowed_users = models.ManyToManyField(User, related_name='viewable_categories')

    def __str__(self):
        return self.name

class Product(models.Model):
    # 定义字段（表的列）

    # 标题：一个最大长度为 100 的文本字段
    name = models.CharField(max_length=100)

    # 描述：一个长文本字段
    description = models.TextField()

    # 价格：一个十进制数字字段，最大位数10位，小数点后2位
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # 上架日期：一个日期时间字段，创建时自动设置为当前时间
    created_at = models.DateTimeField(auto_now_add=True)

    # 添加图片字段，default 可以设置一张默认图（需存放在 media 目录下）
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')

    # 重写 __str__ 方法，使其在管理后台显示更友好的名称
    def __str__(self):
        return self.name

    def clean(self):
        # 文档推荐的模型层验证
        if self.price < 0:
            raise ValidationError("价格不能为负数！")

    def get_display_price(self):
        # 模型方法：方便在模板里直接调用 {{ product.get_display_price }}
        return f"RMB {self.price}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/multiple/')