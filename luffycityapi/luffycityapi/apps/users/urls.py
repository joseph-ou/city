from django.urls import path, re_path
# from rest_framework_jwt.views import obtain_jwt_token#获取jwt 旧版已弃用
#未定义payload之前的写法
# from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

from .views import CustomTokenObtainPairView

urlpatterns = [
    # path('login/', TokenObtainPairView.as_view(),name='login'),
    path('login/', CustomTokenObtainPairView.as_view(),name='login'),
]