from .form import Taomoi, BieuMau_TaoMoi_ThaoLuan
from . models import *
from app.models import *
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class BlogsView(ListView):
    model = Diendan
    template_name = 'blog.html'
    context_object_name = 'dsdd'
    paginate_by =10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_sub=False)
        context['active_category'] = self.request.GET.get('category', '')
        return context


class diendan_cacchude_view(ListView):
    model = Chude
    context_object_name = 'ccd'
    template_name = 'cac_chu_de.html'
    paginate_by = 10
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        kwargs['dd'] = self.dien_dan
        
        return super().get_context_data(**kwargs)
    
    def get_queryset(self) -> QuerySet[Any]:
        self.dien_dan = get_object_or_404(Diendan, pk=self.kwargs.get('id'))
        queryset = self.dien_dan.cac_chude.order_by('lan_capnhat_cuoi').annotate(replies=Count('cac_thaoluan') - 1)
        
        return queryset


@login_required
def tao_chude_moi(req,id):
    dd = get_object_or_404(Diendan, id=id)
    if req.method == 'POST':
        form = Taomoi(req.POST)
        if form.is_valid():
            cd = form.save(commit=False)
            cd.dien_dan = dd
            cd.tao_boi = req.user
            cd.save()

            tl = Thaoluan.objects.create(
                nd = form.cleaned_data.get('noi_dung'),
                chu_de = cd,
                tao_boi = req.user,)
            
            return redirect('diendan_cac_chude', id=dd.id)
    else:
        form = Taomoi()

    return render(req, 'tao_chude_moi.html', {'dd':dd, 'form': form})


class chude_thaoluan(ListView):
    model = Thaoluan
    context_object_name = 'ctl'
    template_name = 'chude_thaoluan.html'
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        self.chu_de.luot_xem +=1
        self.chu_de.save()
        kwargs['cd'] = self.chu_de
        
        return super().get_context_data(**kwargs)
    
    def get_queryset(self):
        self.chu_de = get_object_or_404(Chude, dien_dan__pk=self.kwargs.get('ddpk'), pk=self.kwargs.get('cdpk'))
        queryset = self.chu_de.cac_thaoluan.order_by('ngay_tao')
        return queryset

# ktra xem có fai thành viên diễn đàn

@login_required
def tao_thaoluan_moi(req, ddpk, cdpk):
  cd = get_object_or_404(Chude, pk=cdpk)
  if req.method == 'POST':
    form = BieuMau_TaoMoi_ThaoLuan(req.POST)
    if form.is_valid():
      tl = form.save(commit=False)
      tl.chu_de = cd
      tl.tao_boi = req.user
      tl.save()
      
      return redirect('chude_thaoluan', ddpk=ddpk, cdpk=cdpk)
  else:
    form = BieuMau_TaoMoi_ThaoLuan()
  
  return render(req, 'thaoluan_moi.html', {'cd': cd, 'form': form})

class sua_nd_thaoluan(UpdateView):
    model = Thaoluan
    fields = ['nd']
    template_name = 'sua_nd_thaoluan.html'
    pk_url_kwarg = 'tlpk'
    context_object_name = 'tl'

    def form_valid(self, form):
        tl = form.save(commit=False)
        tl.tao_boi = self.request.user
        tl.ngay_capnhat = timezone.now()
        tl.save()

        return redirect('chude_thaoluan', ddpk = tl.chu_de.dien_dan.pk, cdpk = tl.chu_de.pk)
