from django.contrib import admin

from .models import *

# hiển thị noi dung trong admin 
class product(admin.ModelAdmin):
    list_display = ('product_name','price', 'digital')
    # lọc 
    list_filter = ('digital', )
    # tìm kiếm 
    search_fields = ('product_name', )


class order(admin.ModelAdmin):
    list_display = ('customer', 'date_order', 'complete')
    list_filter = ('date_order', )
    search_fields = ('customer__customer_name', )

class orderitem(admin.ModelAdmin):
    list_display = ('product', 'order', 'category', 'quantity', 'get_total', 'date_added')
    list_filter = ('date_added', )
    search_fields = ('product__product_name', )

class shipping(admin.ModelAdmin):
    list_display = ('customer', 'address', 'city', 'phone', 'state', 'date_added')
    # list_filter = ('date_added', )
    # tìm kiếm 
    search_fields = ('customer__customer_name', )

class category(admin.ModelAdmin):
    list_display = ( 'name_category', 'is_sub')
    search_fields = ('name_category', )

class wishlist(admin.ModelAdmin):
    list_display = ('product', 'user')
    search_fields = ('product__product_name', )
    
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'content')
    search_fields = ('full_name', 'email')
    list_filter = ('content',)


# đăng ký trong admin
admin.site.register(Product, product)
admin.site.register(Order, order)
admin.site.register(Orderitem, orderitem)
admin.site.register(Shipping, shipping)
admin.site.register(Category, category)
admin.site.register(Wishlist, wishlist)
admin.site.register(Contact, ContactAdmin)
