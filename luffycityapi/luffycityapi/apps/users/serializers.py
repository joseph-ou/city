import re

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

from luffycityapi.utils.tencentcloudapi import TencentCloudAPI, TencentCloudSDKException #添加验证腾讯云的验证码ticket和randstr

import constants
from django_redis import get_redis_connection

#自定义jwt载荷 在payload里面添加自己所需要的内容
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # 获取默认 token（包含 user_id、exp、iat、jti 等）
        token = super().get_token(user)

        # 移除 user_id（默认字段）
        if 'user_id' in token:
            del token['user_id']

        # 添加自定义字段（比如 username）
        if hasattr(user, 'username'):
            token['username'] = user.username

        # 可选：添加其他字段
        if hasattr(user,'avatar'):
            token['avatar'] = user.avatar.url if user.avatar else ''

        if hasattr(user, 'money'):
            token['money'] = float(user.money)

        if  hasattr(user, 'credit'):
            token['credit'] = user.credit

        return token



#用户注册
class UserRegisterSerializer(serializers.ModelSerializer):
    '''用户注册的序列化器'''
    #因为用户列表里面没有re_password,sms_code,token 所以要自定义
    re_password = serializers.CharField(required=True, write_only=True)
    sms_code = serializers.CharField(min_length=4, max_length=6, required=True, write_only=True)
    token = serializers.CharField(read_only=True)
    #集成防水墙功能
    #ticket = serializers.CharField(required=True, write_only=True, help_text="滑块验证码的临时凭证")
    #randstr = serializers.CharField(required=True, write_only=True, help_text="滑块验证码的随机字符串")


    class Meta:
        model = User
        # fields = '__all__'
        fields = ['mobile','password','re_password','sms_code','token']
        #fields = ["mobile", "password", "re_password", "sms_code", "token", "ticket", "randstr"] #启用防水墙时用这个
        extra_kwargs = {
            'mobile':{'required':True,'write_only':True},
            'password':{'required':True,'write_only':True},
        }

    def validate_mobile(self, value):
        '''字段级验证 针对特定字段mobile进行查 validate_<field_name>(self,value)'''
        if not re.match(r'^1[3-9]\d{9}$', value):
            #手机号格式错误
            raise serializers.ValidationError(detail='Mobile format error:手机号格式错误',code='mobile')


        #手机号是否已经注册
        if User.objects.filter(mobile=value).exists():
            raise serializers.ValidationError(detail='Mobile already registered:手机号已经注册')
        return value


    def validate(self, data):#data是初步验证后的字段数据
        """验证客户端数据"""
        # 密码确认
        password=data.get('password')
        re_password=data.get('re_password')
        if password != re_password:
            raise serializers.ValidationError(detail="密码和确认密码不一致！", code="password")

        # todo 验证防水墙验证码
        # api = TencentCloudAPI()
        # result = api.captcha(
        #     data.get("ticket"),
        #     data.get("randstr"),
        #     self.context['request']._request.META.get("REMOTE_ADDR"),  # 客户端IP
        # )
        #
        # if not result:
        #     raise serializers.ValidationError(detail="滑块验证码校验失败！")

        # todo 验证短信验证码
        redis=get_redis_connection('sms_code')
        mobile=data.get('mobile')
        code = redis.get(f"sms_{mobile}")
        if code is None:
            '''获取不到验证码 说明验证码过期或者失效'''
            raise serializers.ValidationError(detail="短信验证码失效或过期", code="sms_code")

        # 从redis提取的数据，字符串都是bytes类型，所以decode
        if code.decode() != data.get("sms_code"):
            raise serializers.ValidationError(detail="短信验证码错误！", code="sms_code")
        print(f"code={code.decode()}, sms_code={data.get('sms_code')}")
        # 删除掉redis中的短信，后续不管用户是否注册成功，至少当前这条短信验证码已经没有用处了
        redis.delete(f"sms_{mobile}")

        return data



    def create(self, validated_data):
        '''保存用户信息并完成注册'''
        """保存用户信息，完成注册"""
        mobile = validated_data.get("mobile")
        password = validated_data.get("password")

        user = User.objects.create_user(
            username=mobile,
            mobile=mobile,
            avatar=constants.DEFAULT_USER_AVATAR,
            password=password,
        )

        return user


    def get_token(self, user):
        '''使用自定义的token'''
        # 注册成功以后，免登陆
        token = CustomTokenObtainPairSerializer.get_token(user)
        return str(token)

