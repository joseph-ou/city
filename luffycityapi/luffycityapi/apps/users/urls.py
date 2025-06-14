from django.urls import path, re_path
# from rest_framework_jwt.views import obtain_jwt_token#获取jwt 旧版已弃用
#未定义payload之前的写法
# from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

from .views import CustomTokenObtainPairView,MobileRegisterCheckAPIView,UserRegisterAPIView

urlpatterns = [
    # path('login/', TokenObtainPairView.as_view(),name='login'),
    path('login/', CustomTokenObtainPairView.as_view(),name='login'),
    re_path(r'^mobile/(?P<mobile>1[3-9]\d{9})/$',MobileRegisterCheckAPIView.as_view(),), #(?P<XXXX>...) 是命题捕获组 将括号后面...的元素捕获并命名为XXXX 在后端get中可以直接调用
    path('register/',UserRegisterAPIView.as_view(),name='register'),
]