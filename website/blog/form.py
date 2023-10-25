import django.forms as forms
from .models import Chude, Thaoluan

class Taomoi(forms.ModelForm):
    noi_dung = forms.CharField(label='Nội dung', widget=forms.Textarea(attrs={'row':5, 
                                                            'placeholder': 'Nhập nội dung'}),
                            max_length=5000,
                            help_text='Độ dài không quá 5000 từ')

    def __init__(self, *args, **kwargs):
        super(Taomoi, self).__init__(*args, **kwargs)
        self.fields['ten_chude'].label = "Tên chủ đề"
    class Meta:
        model = Chude
        # thuoc tinh hien thi
        fields = ['ten_chude', 'noi_dung']

        
class BieuMau_TaoMoi_ThaoLuan(forms.ModelForm):   
    def __init__(self, *args, **kwargs):
        super(BieuMau_TaoMoi_ThaoLuan, self).__init__(*args, **kwargs)
        self.fields['nd'].label = "Nội dung"

    class Meta:
        model = Thaoluan
        fields = ['nd']
