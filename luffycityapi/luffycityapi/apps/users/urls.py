from django.urls import path, re_path
# from rest_framework_jwt.views import obtain_jwt_token#获取jwt 旧版已弃用
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from . import views

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(),name='login'),
]