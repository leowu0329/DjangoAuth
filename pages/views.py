from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

@login_required  # 這個裝飾器會自動檢查登入狀態
def home_page(request):
    return render(request, 'home.html')  # 假設你的首頁模板是 home.html
