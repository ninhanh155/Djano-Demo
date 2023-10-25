from django.db import models
from django.contrib.auth.models import User

from django.utils.text import Truncator
# Create your models here.
class Diendan(models.Model):
    ten_diendan = models.CharField(max_length=100, unique=True)
    mota = models.CharField(max_length=1000000)
    ngaytao = models.DateTimeField(auto_now_add=True)
    def soluong_thaoluan(self):
        return Thaoluan.objects.filter(chu_de__dien_dan = self).count()

    def __str__(self):
        return self.ten_diendan

        # tạo diễn đàn trong shell
# from faker import Faker
# >>> for _ in  range(0,500):
# ...     Diendan.objects.create(ten_diendan = faker.sentence(), mota = faker.paragraph())

class Chude(models.Model):
    ten_chude = models.CharField(max_length=100)
    lan_capnhat_cuoi = models.DateTimeField(auto_now_add=True)
    luot_xem = models.PositiveIntegerField(default=0)
    # moi quan he vs dien dan
    # khai baos khóa ngoài
    dien_dan = models.ForeignKey(Diendan, related_name='cac_chude', 
                                on_delete=models.CASCADE) # rang buoc qh du lieu mang tinh toan ven
    # mqh vs tao chu de
    tao_boi = models.ForeignKey(User, related_name= 'tao_chude_moi', on_delete= models.CASCADE)
    def __str__(self):
        return self.ten_chude
        
class Thaoluan(models.Model):
    nd = models.TextField(max_length=5000)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_capnhat = models.DateTimeField(null=True)
    # qh vs cac thảo luận
    chu_de = models.ForeignKey(Chude, related_name= 'cac_thaoluan', on_delete=models.CASCADE)
    tao_boi = models.ForeignKey(User, related_name='tao_thaoluan', on_delete=models.CASCADE)
    thanhvien_capnhat = models.ForeignKey(User, related_name='capnhat_boi', null=True , on_delete=models.CASCADE)



    def __str__(self):
        truncated_message = Truncator(self.nd)
        
        return truncated_message.chars(30)
