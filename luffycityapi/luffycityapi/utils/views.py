'''基本的视图类'''

#重写视图类对页面缓存进行配置
import constants
from rest_framework.generics import ListAPIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page




class CacheListAPIView(ListAPIView):
    '''列表视图缓存类'''

    @method_decorator(cache_page(constants.LIST_PAGE_CACHE_TIME))
    def get(self, request, *args, **kwargs):
        #重写ListAPIView的get方法 但是不改动源代码 仅装饰
        return super().get(request, *args, **kwargs)