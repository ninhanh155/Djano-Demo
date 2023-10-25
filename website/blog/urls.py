from django.urls import path
from . import views

urlpatterns = [
    # path('tintuc/',views.blogs, name='blog'),
     path('Tintuc/', views.BlogsView.as_view(), name= 'blog'),
    path('Tintuc/<int:id>', views.diendan_cacchude_view.as_view(), name= 'diendan_cac_chude'),
    path('Tintuc/<int:id>/tao_chude',views.tao_chude_moi, name='tao_chu_de_moi'),
    path('Tintuc/<int:ddpk>/chude/<int:cdpk>/', views.chude_thaoluan.as_view(), name= 'chude_thaoluan'),
    path('Tintuc/<int:ddpk>/chude/<int:cdpk>/thaoluan/',views.tao_thaoluan_moi, name= 'tao_thaoluan_moi'),
    path('Tintuc/<int:ddpk>/chude/<int:cdpk>/thaoluan/<int:tlpk>/sua_nd_thaoluan/',views.sua_nd_thaoluan.as_view(), name='sua_nd_thaoluan'),
]