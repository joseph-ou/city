#创建路由
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('test', views.HomeView.as_view(), name='home'),

]