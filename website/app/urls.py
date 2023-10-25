from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .form import *

urlpatterns = [
    path('', views.home.as_view(), name='home'),
    path('cart/', views.cart, name='cart'),
    path('product/', views.product.as_view(), name='product'),
    # làm tăng số lượng sp trong giỏ hàng
    path('update_item/', views.updateItem, name='update_item'),
    path('checkout/', views.checkout, name='checkout'),
    # path('checkout_sucess/', views.checkout_sucess, name='checkout_sucess'),
    path('order/', views.order, name='order'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('search/', views.search, name= 'search'),
    path('category/', views.category, name= 'category'),
    path('chitiet/<int:product_id>/', views.detail, name= 'chitiet'),
    path('chitiet/<int:product_id>/comment/', views.tao_thao_luan, name='binh_luan'),
#  quản trị
    path('dangky/', views.dangky, name= 'dangky'),
    path("dangxuat/", auth_views.LogoutView.as_view(), name='dangxuat'),
    path("dangnhap/", auth_views.LoginView.as_view(template_name='dangnhap.html'), name='dangnhap'),
    path('taikhoan/', views.Taikhoan.as_view(), name='taikhoan'),
    path('doimatkhau/',auth_views.PasswordChangeView.as_view(template_name='thaylaimatkhau.html',form_class = Bieumau_doimatkhau, success_url = '/hoanthanhdoimk'), name='thaylaimatkhau'),
    path("hoanthanhdoimk/",auth_views.PasswordResetCompleteView.as_view( template_name='hoanthanh_doimk.html'),name='password_reset_complete'), 
    # quên mk
    path("quenmatkhau/", auth_views.PasswordResetView.as_view(template_name='quenmatkhau.html',
                                                                email_template_name= 'guiemail.html',
                                                                subject_template_name='quenmatkhau.txt'), name='quenmatkhau'),              
                                                                 
    path("daguilink/", auth_views.PasswordResetDoneView.as_view(template_name='guilink.html'), name = 'password_reset_done'),

    path("doimatkhau/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name='doimatkhau.html'),name='doimatkhau'),
    path("htdmk",auth_views.PasswordResetCompleteView.as_view( template_name='hoanthanh_doimk.html'),name='password_reset_complete'), 
    # phan hoi
    path('lien-he/', views.contact, name='contact'),

    path('pluswishlist/', views.plus_wishlist),
    path('minuswishlist/', views.minus_wishlist),
    path('wishlist/', views.wishlist, name= 'yeuthich'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('thongke/',views.revenue_by_day,name='thongke'),
     path('order-history/', views.order_history, name='order_history'),
    
    
]