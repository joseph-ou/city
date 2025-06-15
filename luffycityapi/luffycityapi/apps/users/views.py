from django.shortcuts import render


from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
#腾讯验证码
from luffycityapi.utils.tencentcloudapi import TencentCloudAPI,TencentCloudSDKException

from .models import User #获取自定义的user模型
from .serializers import UserRegisterSerializer

# Create your views here.

#自定义载荷的jwt 同时自定义post方法集成腾讯验证码功能
class CustomTokenObtainPairView(TokenObtainPairView):
    """用户登录视图 post分为集成验证码功能和不集成的"""
    serializer_class = CustomTokenObtainPairSerializer


    # def post(self, request, *args, **kwargs):
    #     # 校验用户操作验证码成功以后的ticket临时票据
    #     try:
    #         api = TencentCloudAPI()
    #         result = api.captcha(
    #             request.data.get("ticket"),
    #             request.data.get("randstr"),
    #             request._request.META.get("REMOTE_ADDR"),
    #         )
    #         if result:
    #             # 验证通过
    #             print("验证通过")
    #             # 登录实现代码，调用父类实现的登录视图方法
    #             return super().post(request, *args, **kwargs)
    #         else:
    #             # 如果返回值不是True，则表示验证失败
    #             raise TencentCloudSDKException
    #     except TencentCloudSDKException as err:
    #         return Response({"errmsg": "验证码校验失败！"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self,request,*args,**kwargs):
        return super().post(request,*args,**kwargs)



#手机号注册验证
class MobileRegisterCheckAPIView(APIView):

    def get(self,request,mobile):
        # 获取手机号注册信息
        #因为是get请求从url获取字段所以mobile直接引入

        try:
            User.objects.get(mobile=mobile)
            return Response({"msg": "当前手机号已注册"}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
        # 如果查不到该手机号的注册记录，则证明手机号可以注册使用
            return Response({"msg": "注册状态：ok"}, status=status.HTTP_200_OK)


class UserRegisterAPIView(APIView):
    '''完整写法'''
    def post(self,request,*args,**kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            # print("register success")
            # print(serializer.validated_data)

            #生成token(access) 实现注册后自动登录的状态
            access=serializer.get_token(user)

            response_data ={
                'access' : access,
                'mobile' : serializer.validated_data['mobile'],
                'password' : serializer.validated_data['password'],
                're_password': serializer.validated_data['re_password'],
                'sms_code': serializer.validated_data['sms_code'],
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserRegisterAPIView(CreateAPIView):
#
#     #主要提供模型信息（比如 User 模型 说明提交的是user模型的数据），而不是直接查询数据
#     queryset = User.objects.all()
#     #使用自定义的序列化器
#     serializer_class = UserRegisterSerializer
#
#     #如果需要更精确的范围可以重写get_queryset方法
#     def get_queryset(self):
#         return User.objects.filter(is_active=True)
#
#     #如果需要在创建前添加条件筛选可以重写perform_create方法
#     # def perform_create(self, serializer):
#     #     if User.objects.filter(mobile=serializer.validated_data['mobile']).exists():
#     #         raise ValidationError("手机号已注册")
#     #     serializer.save()