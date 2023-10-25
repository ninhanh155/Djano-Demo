from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
from .form import *
from django.contrib.auth import login as qldangnhap
from django.views.generic import UpdateView, ListView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import json
import random
import string
import time
from django.utils import timezone
from datetime import datetime, timedelta ,date
from django.db.models import F,Sum ,Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.db.models.functions import TruncMonth

class home(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
    paginate_by =8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_sub=False)
        context['active_category'] = self.request.GET.get('category', '')
        return context

class product(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'products'
    paginate_by =20
    ordering = ['price']  # Mặc định sắp xếp theo giá tăng dần

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_sub=False)
        context['active_category'] = self.request.GET.get('category', '')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.GET.get('sort', '')  # Lấy tham số sort từ URL

        if sort == 'price_asc':
            queryset = queryset.order_by('price')  # Sắp xếp theo giá tăng dần
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')  # Sắp xếp theo giá giảm dần

        return queryset 

@login_required
def cart(req):
    if req.user.is_authenticated:
        customers = req.user
        order, created = Order.objects.get_or_create(customer=customers, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        cartItems = order.get_cart_items
    categories = Category.objects.filter(is_sub = False)
    active_category = req.GET.get('category', '')
    return render(req, 'cart.html', locals())

def remove_from_cart(request, product_id):
    customer = request.user
    order = Order.objects.get(customer=customer, complete=False)
    product = Product.objects.get(id=product_id)
    Orderitem.objects.filter(order=order, product=product).delete()
    return redirect('cart')


def checkout(req):
    if req.user.is_authenticated:
        customer = req.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        # kiểm tra giỏ hàng trống
        if cartItems == 0: 
            return render(req, 'empty_cart.html')

        if req.method == 'POST':
            ordered_items = order.orderitem_set.all()
            # chứa các sp đã mua vào ds
            purchased_items = []
            
            for item in ordered_items:
                # lưu các sp vào admin
                product = item.product
                category = item.category
                quantity = item.quantity
                order_item = Orderitem(
                    product=product,
                    order=order,
                    category=category,
                    quantity=quantity,
                )
                # lưu và thêm vào admin
                order_item.save()
                purchased_items.append(item)

            # Xóa các sp đã mua khỏi giỏ hàng
            for item in purchased_items:
                item.delete()

            # Cập nhật trạng thái đơn hàng
            order.complete = True
            order.save()

            # Lưu thông tin vận chuyển vào admin
            shipping_info = Shipping(
                order=order,
                customer=customer,
                address=req.POST.get('address'),
                city=req.POST.get('city'),
                state=True,
                phone=req.POST.get('phone'),
            )
            shipping_info.save()
           
            cart_total = order.get_cart_total()

            return render(req, 'checkout_success.html', locals())
    else:
        items = []
        cartItems = order.get_cart_items()

    categories = Category.objects.filter(is_sub=False)
    active_category = req.GET.get('category', '')
    return render(req, 'checkout.html', locals())


def order(req):
    if req.user.is_authenticated:
        customer = req.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        order_code = generate_order_code()
    else:
        items = []
        cartItems = order.get_cart_items
    categories = Category.objects.filter(is_sub=False)
    active_category = req.GET.get('category', '')
    return render(req, 'order.html', locals())



def dangky(req):
    if req.method == 'POST' :
        ucf = Bieumau_dangky_thanhvien(req.POST)
        if ucf.is_valid():
            user = ucf.save()
            qldangnhap(req, user)

            return redirect('home')
    else:
        ucf = Bieumau_dangky_thanhvien()

    return render(req, 'dangky.html', {'form': ucf})


@method_decorator(login_required, name='dispatch')
class Taikhoan(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email' )
    template_name = 'taikhoan.html'
    success_url = reverse_lazy('taikhoan')

    def get_object(self):
        return self.request.user

def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    customers = request.user
    product = Product.objects.get(id= productID)
    order, created = Order.objects.get_or_create(customer= customers, complete= False)
    orderitem, created = Orderitem.objects.get_or_create(order= order, product= product)
    if action == 'add':
        orderitem.quantity += 1
    elif action == 'remove':
        orderitem.quantity -= 1
    orderitem.save()
    if orderitem.quantity <= 0:
        orderitem.delete()

    return JsonResponse('added', safe=False)

def search(req):
    if req.method == "POST":
        searched = req.POST['searched']
        keys = Product.objects.filter(product_name__contains = searched)
    products = Product.objects.all()
    categories = Category.objects.filter(is_sub = False)
    active_category = req.GET.get('category', '')
    return render(req, 'timkiem.html', locals())

def category(req):
    categories = Category.objects.filter(is_sub = False)
    active_category = req.GET.get('category', '')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    # hiển thị số lượng sp trong cart

    
    return render (req, 'danhmuc.html' , locals())
def detail(req, product_id):

    cd = get_object_or_404(Product, pk=product_id)
    product = Product.objects.filter(id=product_id)
    wishlist = Wishlist.objects.filter(product=product_id, user=req.user)
    categories = Category.objects.filter(is_sub=False)
    active_category = req.GET.get('category', '')
    
    comment = Comment.objects.filter(product=cd)
    if req.user.is_authenticated:
        comment = comment.filter(user=req.user)

    return render(req, 'chitiet.html', locals())
    
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Xử lý dữ liệu liên hệ từ form gửi đi
            name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['content']
            
            # lưu vào cơ sở dữ liệu
            contact = Contact(full_name=name, email=email, content=message)
            contact.save()
            
            # Hiển thị thông báo thành công hoặc chuyển hướng đến trang khác
            return render(request, 'contact_sucess.html')
    else:
        form = ContactForm()
    
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')
    return render(request, 'contact.html', locals())

@login_required
def wishlist(req):
    user = req.user
    wishlist = user.wishlist.all()
    categories = Category.objects.filter(is_sub=False)
    active_category = req.GET.get('category', '')
    if wishlist.count() == 0: 
        return render(req, 'wishlist_empty.html', locals())
    return render(req, 'wishlist.html', locals())

def remove_from_wishlist(request, product_id):
    user = request.user
    wishlist_item = Wishlist.objects.filter(user=user, product_id=product_id)
    if wishlist_item.exists():
        wishlist_item.delete()
        
    return redirect('yeuthich')


def plus_wishlist(req):
    if req.method == "GET":
        prod_id = req.GET['prod_id']
        product = Product.objects.get(id=prod_id)

        user = req.user
        wishlist, created = Wishlist.objects.get_or_create(user=user, product=product)
        if created:
            data = {
                'message': 'Product added to wishlist successfully'
            }
        else:
            data = {
                'message': 'Product already exists in wishlist'
            }
        return JsonResponse(data)

def minus_wishlist(req):
    if req.method == "GET":
        prod_id = req.GET['prod_id']
        product = Product.objects.get(id=prod_id)

        user = req.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data = {
            'message': 'Product removed from wishlist successfully'
        }
        return JsonResponse(data)


@login_required
def tao_thao_luan(req,product_id):
    cd = get_object_or_404(Product,pk = product_id)
    # product = Product.objects.filter(id=pk)
    if req.method == 'POST':
        # product = Product.objects.filter(id=pk)
        binh_luan = req.POST.get('binh_luan')
        # product = req.product
        user = req.user
        comment = Comment(user = user ,product = cd ,noi_dung = binh_luan)
        comment.save()
        return redirect('chitiet',product_id = product_id)
    categories = Category.objects.filter(is_sub=False)
    active_category = req.GET.get('category', '')
    return render(req, 'chitiet.html', locals())


def revenue_by_day(request):
    # Lấy ngày hiện tại
    current_date = timezone.now().date()

    # Lấy ngày bắt đầu của khoảng thời gian (7 ngày trước)
    start_date = current_date - timedelta(days=7)

    # Tổng số sản phẩm
    total_products = Product.objects.count()

    # Tổng số khách hàng đã đăng ký tài khoản
    total_registered_users = User.objects.count()

    # Tổng tiền của sản phẩm đã bán
    total = (
        Orderitem.objects
        .filter(date_added__date__range=[start_date, current_date])
        .annotate(month=TruncMonth('date_added'))
        .values('month')
        .annotate(total_sales=Sum(F('quantity') * F('product__price')))
        .order_by('month')
    )

    # Lấy danh sách các ngày và tổng tiền của sản phẩm đã bán 
    sales_by_day = (
        Orderitem.objects
        .filter(date_added__date__range=[start_date, current_date])
        .values('date_added__date')
        .annotate(total_sales=Sum(F('quantity') * F('product__price')))
        .order_by('date_added__date')
    )

    return render(request, 'admin/chart.html', locals())

def order_history(req):
    order_items = Order.objects.filter(customer=req.user)
    categories = Category.objects.filter(is_sub=False)
    active_category = req.GET.get('category', '')
    return render(req, 'order_history.html', locals())