from django.contrib import admin

# Register your models here.
from .models import Diendan, Chude, Thaoluan

class DiendanAdmin(admin.ModelAdmin):
    list_display = ('ten_diendan', 'ngaytao')
    search_fields = ('ten_diendan', )

class ChudeAdmin(admin.ModelAdmin):
    list_display = ('ten_chude', 'tao_boi' ,'lan_capnhat_cuoi', 'luot_xem')
    search_fields = ('ten_chude', )


class ThaoluanAdmin(admin.ModelAdmin):
    list_display = ('tao_boi','nd', 'ngay_tao', 'ngay_capnhat')
    search_fields = ('tao_boi__username', )


admin.site.register(Diendan, DiendanAdmin)
admin.site.register(Chude, ChudeAdmin)
admin.site.register(Thaoluan, ThaoluanAdmin)