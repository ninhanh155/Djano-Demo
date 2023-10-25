from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# doanh mục/ phân loại sp
class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_categories', null = True, blank=True)
    # ktra xem có fai doanh mục con hay k
    is_sub  = models.BooleanField(default=True)
    name_category = models.CharField(max_length=200, null=True)
    # dg dẫn đã đc tối ưu, đảm bảo là đg dẫn duy nhất
    slug = models.SlugField(max_length=200, unique=True)  
    def __str__(self):
        return self.name_category
        

# sản phẩm
class Product(models.Model):
    product_name = models.CharField(max_length=200, null= True)
    # đon giá
    price = models.FloatField()
    # bán nhiều loại sản phẩm
    digital = models.BooleanField(default=True)
    image = models.ImageField(null=True, blank=True)
    category = models.ManyToManyField(Category, related_name='product')
    detail = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.product_name
    # dieu chinh thuoc tinh
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
        
class Order(models.Model):
    # trường khóa gọi class khách hàng
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    # khách hàng đã mua xog chưa
    complete = models.BooleanField(default=True)
    # lưu thông tin ng mua đã order
    transaction_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.customer)

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

# ng mua order nhiều sp
class Orderitem(models.Model):
    # trường khóa gọi class 
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    # số lg mua
    quantity = models.IntegerField(default=0, null=True, blank=True)
    # ngày đặt hàng
    date_added = models.DateTimeField(auto_now_add=True)
        
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total 
        
class Shipping(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.BooleanField(default=True)
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Số điện thoại phải gồm 10 chữ số.")
    phone = models.CharField(max_length=10, validators=[phone_regex], null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    @property
    def get_wishlist_items(self):
        orderitems = self.wishlist_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank= False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank= False)
    noi_dung = models.TextField(max_length=400)
    def __str__(self):
        return self.noi_dung

class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()

    def __str__(self):
        return self.full_name
