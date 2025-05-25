#创建路由
from django.urls import path, re_path
from . import views

urlpatterns = [
    # path('test', views.HomeView.as_view(), name='home'),
    path('nav/header/', views.NavHeaderView.as_view(), name='Nav_Header'),
    path('nav/footer/', views.NavFooterView.as_view(), name='Nav_Footer'),

]