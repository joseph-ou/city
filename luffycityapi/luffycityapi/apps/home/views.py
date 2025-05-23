# from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework import status
#res_framework
from rest_framework.views import APIView
from rest_framework.response import Response

#对日志调用
import logging
logger=logging.getLogger('django')

# Create your views here.
class HomeView(APIView):

    def get(self, request):
        """测试代码"""
        #测试日志功能
        # logger.error('error:')
        # logger.info('info:')

        redis=get_redis_connection('sms_code')
        user=redis.lrange('test1',0,-1)


        message='csndm'
        return Response({"message": user,'status':status.HTTP_200_OK})