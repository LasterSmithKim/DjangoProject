# products/forms.py

from django import forms
from .models import Product, ProductImage  # 导入第二阶段的 Model
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError

# 方法 A：使用 ModelForm（推荐）
# ModelForm 可以根据现有的 Model 自动生成表单字段和验证规则
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        # 指定要在表单中显示的字段
        fields = ['name', 'description','price','image', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',}),
            'price': forms.NumberInput(attrs={'class': 'form-control',}),
            'description': forms.Textarea(attrs={'class': 'form-control','rows': 3,  # 设置显示行数
            }),
        }
        # 汉化表单的 Label
        labels = {
            'name': '商品名称',
            'price': '价格',
            'description': '详情描述',
        }
        # 如果你想显示所有字段，可以使用 fields = '__all__'



    # 进阶：自定义字段验证 (Clean method)
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 10:
            raise ValidationError("价格太低了！本商城不售卖 10 元以下商品。")
        return price

    # 进阶：跨字段验证 (针对整个表单的验证)
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')

        if name and description and name in description:
            # 如果描述里重复了标题，抛出一个非字段错误
            raise ValidationError("描述内容不应包含重复的商品名称。")



ProductImageFormSet = inlineformset_factory(
    Product, ProductImage, fields=['image'], extra=1, can_delete=True
)