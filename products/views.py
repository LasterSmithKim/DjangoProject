from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404 # 导入 redirect 用于重定向
from .models import Product,ProductImage  # 导入我们第二阶段创建的 Model
from .forms import ProductForm,ProductImageFormSet # 导入刚刚创建的表单类
from django.contrib.auth.decorators import login_required # 导入装饰器
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets,permissions
from .serializers import ProductSerializer


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/index.html'
    context_object_name = 'products'  # HTML 里依然用 {% for product in products %}

    # 这里的 get_queryset 就是你说的“合成管理器”核心
    def get_queryset(self):
        # 逻辑：
        # 1. 获取当前登录用户 (self.request.user)
        # 2. 找到该用户有权访问的所有分类
        # 3. 过滤出属于这些分类的商品
        return Product.objects.filter(category__allowed_users=self.request.user).distinct()

@login_required # 只有登录用户才能看
def product_list(request):
    # 1. 业务逻辑：从数据库获取所有产品数据（使用 ORM）
    all_products = Product.objects.all()

    # 2.准备上下文（Context）：将数据打包成字典，以便传递给模板
    context = {
        'products': all_products,
        'page_title': '产品列表页'
    }

    # 3. 渲染模板并返回响应：
    # Django 会查找一个名为 'product_list.html' 的模板文件，
    # 并将 context 中的数据注入到模板中
    return render(request, 'products/product_list.html', context)

def product_index(request):
    all_products = Product.objects.all()
    context = {
        'products': all_products,
        'page_title': '产品列表页'
    }
    return render(request, 'products/index.html', context)

@login_required # 只有登录用户才能看
def product_create(request):
    # 检查请求方法：是 GET（刚打开页面）还是 POST（提交了表单）
    if request.method == 'POST':
        # 如果是 POST 请求，将提交的数据绑定到表单实例
        form = ProductForm(request.POST, request.FILES)
        formset = ProductImageFormSet(request.POST, request.FILES)
        files = request.FILES.getlist('images')  # 获取多文件列表

        # 验证数据是否有效（如名称是否为空，价格是否为数字）
        if form.is_valid() and formset.is_valid():
            # 有效则保存数据到数据库（ModelForm 自动处理）
            product = form.save()
            for f in files:
                ProductImage.objects.create(product=product, image=f)
            formset.instance = product  # 将图片集绑定到刚创建的商品上
            formset.save()
            # 保存成功后，重定向到产品列表页（避免重复提交）
            return redirect('products:product_list')  # 使用我们在 urls.py 中定义的 name='product-list'
        else:
            # 💡 增加这两行，保存失败时终端会打印具体的错误原因
            print("主表单错误:", form.errors)
            print("图片集错误:", formset.errors)
    else:
        # 如果是 GET 请求（第一次访问），创建一个空的表单实例
        form = ProductForm()
        formset = ProductImageFormSet()

    # 准备上下文，将表单实例传递给模板
    context = {
        'form': form,'formset': formset
    }
    return render(request, 'products/product_form.html', context)




@login_required # 只有登录用户才能看
def product_detail(request, pk):
    # 使用 get_object_or_404：如果 ID 存在则返回对象，不存在则自动返回 404 页面
    product = get_object_or_404(Product, pk=pk)

    return render(request, 'products/product_detail.html', {'product': product})


@login_required # 只有登录用户才能看
def product_update(request, pk):
    # 1. 获取要修改的对象
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        # 2. 将提交的新数据绑定到【现有对象】实例上
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()  # 这里会自动处理：添加新图、更新旧图、删除勾选了“删除”的图
            print(f"上传的文件名是: {request.FILES.get('image')}")
            return redirect('products:product-detail', pk=product.pk)  # 修改后跳回详情页
    else:
        # 3. GET 请求：用当前数据库里的数据填充表单
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product)

    return render(request, 'products/product_form.html', {'form': form,'formset': formset, 'product': product})


@login_required # 只有登录用户才能看
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        # 用户确认删除
        product.delete()
        return redirect('products:product_list')  # 删除后返回列表

    return render(request, 'products/product_confirm_delete.html', {'product': product})

class ProductViewSet(viewsets.ModelViewSet):
    # queryset = Product.objects.all()
    # serializer_class = ProductSerializer
    # # 添加权限：仅登录用户可写，匿名用户只能看 (GET)
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Product.objects.all()
    # 注意：我们移除了 'queryset = Product.objects.all()' 这一行，
    # 因为我们将使用 get_queryset 方法动态地获取查询集。
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]  # 现在要求所有操作都必须登录

    # 覆盖 get_queryset 方法以实现按用户过滤
    def get_queryset(self):
        """
        这个视图应返回所有当前已认证用户有权访问的产品。
        """
        user = self.request.user
        # 如果用户是匿名的（理论上 IsAuthenticated 权限会阻止，但安全起见），返回空查询集
        if user.is_anonymous:
            return Product.objects.none()

        # 应用你原有的过滤逻辑：
        return Product.objects.filter(category__allowed_users=user).distinct()










