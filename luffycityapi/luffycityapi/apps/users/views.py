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


#手机号短信登录
import random
from django_redis import get_redis_connection
from django.conf import settings

# from ronglianyunapi import send_sms #使用容联云发送
from mycelery.sms.tasks import send_sms #用celery 导入调用异步任务

class SMSAPIView(APIView):
    '''SMS短信登录接口'''
    #处理登录
    def get(self,request,mobile,):
        '''发送短信验证码'''
        redis=get_redis_connection('sms_code')
        # 判断手机短信是否处于发送冷却中[60秒只能发送一条]
        interval = redis.ttl(f"interval_{mobile}")  # 通过ttl方法可以获取保存在redis中的变量的剩余有效期
        if interval != -2:
            return Response(
                {"errmsg": f"短信发送过于频繁，请{interval}秒后再次点击获取!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 基于随机数生成短信验证码
        # code = "%06d" % random.randint(0, 999999)
        #f-string 中的 :06d 是一个格式说明符，表示将数字格式化为 6 位整数，不足 6 位时前面补 0。效果与旧方法 "%06d" 相同。
        code=f"{random.randint(0,9999):04d}"
        #获取短信有效时间
        time=settings.RONGLIANYUN.get('sms_expire')
        #短信发送间隔
        sms_interval=settings.RONGLIANYUN['sms_interval']

        #调用第三方发送短信
        # send_sms(settings.RONGLIANYUN.get('reg_tid'),mobile,datas=(code,time//60))

        #使用celery发送异步任务
        send_sms.delay(settings.RONGLIANYUN.get('reg_tid'),mobile,datas=(code,time//60))



        #将code存储到redis里面
        pipe=redis.pipeline()
        pipe.multi()#开启事务
        pipe.setex(f"sms_{mobile}",time,code)#setex添加了一个过期时间
        pipe.setex(f"interval_{mobile}",sms_interval,'_') #记录发送时间并设置发送间隔
        pipe.execute() #提交事务并把暂存在pipeline的数据一次性提交给redis

        return Response({"msg": "sms_send success"}, status=status.HTTP_200_OK)
