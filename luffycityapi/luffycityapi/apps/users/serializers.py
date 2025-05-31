from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


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