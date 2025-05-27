# from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework import status
#res_framework
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.generics import ListAPIView
from .models import Nav, Banner
from .serializers import NavModelSerializer, BannerModelSerializer

#常量配置
import constants

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


class NavHeaderView(ListAPIView):
    '''顶部导航视图'''
    queryset = Nav.objects.filter(position=constants.NAV_HEADER_POSITION,is_show=True,is_deleted=False).order_by('orders','-id')[:constants.NAV_HEADER_SIZE]
    serializer_class = NavModelSerializer

class NavFooterView(ListAPIView):
    '''底部导航视图'''
    queryset = Nav.objects.filter(position=constants.NAV_FOOTER_POSITION,is_show=True,is_deleted=False).order_by('orders','-id')[:constants.NAV_FOOTER_SIZE]
    serializer_class = NavModelSerializer


class BannerView(ListAPIView):
    '''轮播图视图'''

    queryset = Banner.objects.filter(is_show=True, is_deleted=False).order_by('orders','-id')[:constants.BANNER_SIZE]
    serializer_class = BannerModelSerializer
