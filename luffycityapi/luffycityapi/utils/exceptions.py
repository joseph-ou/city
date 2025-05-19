from rest_framework.views import exception_handler, APIView
from django.db import DatabaseError

from rest_framework.response import Response
from rest_framework import status

import logging
logging=logging.getLogger('django')


def custom_exception_handler(exc, context):
    """
    自定义异常处理
    :param exc: 异常类
    :param context: 抛出异常的上下文
    :return: response响应对象
    """
    #调用drf框架原生的异常处理方法
    response = exception_handler(exc, context)

    if response is None:
        # view = context.get("view")
        view = context['view']

        #判断是否发生数据库异常
        if isinstance(exc,DatabaseError):

            logging.error('[%s] %s' %(view,exc))
            response = Response({'message': '服务器内部错误'},status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response