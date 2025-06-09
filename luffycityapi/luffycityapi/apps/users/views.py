from django.shortcuts import render

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

from rest_framework.response import Response
from rest_framework import status
#腾讯验证码
from luffycityapi.utils.tencentcloudapi import TencentCloudAPI,TencentCloudSDKException


# Create your views here.

#自定义载荷的jwt 同时自定义post方法集成腾讯验证码功能
class CustomTokenObtainPairView(TokenObtainPairView):
    """用户登录视图 """
    serializer_class = CustomTokenObtainPairSerializer


    def post(self, request, *args, **kwargs):
        # 校验用户操作验证码成功以后的ticket临时票据
        try:
            api = TencentCloudAPI()
            result = api.captcha(
                request.data.get("ticket"),
                request.data.get("randstr"),
                request._request.META.get("REMOTE_ADDR"),
            )
            if result:
                # 验证通过
                print("验证通过")
                # 登录实现代码，调用父类实现的登录视图方法
                return super().post(request, *args, **kwargs)
            else:
                # 如果返回值不是True，则表示验证失败
                raise TencentCloudSDKException
        except TencentCloudSDKException as err:
            return Response({"errmsg": "验证码校验失败！"}, status=status.HTTP_400_BAD_REQUEST)