'''作为第三方模块celery集成到项目中 mycelery为独立模块调用'''

from celery import Celery
import os

#必须在实例化celery应用对象前执行
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luffycityapi.settings.dev')


#实例化celery对象
app = Celery('luffycityapi')
# 指定任务的队列名称
app.conf.task_default_queue = 'Celery'
# 也可以把配置写在django的项目配置中
app.config_from_object('django.conf:settings', namespace='CELERY') # 设置django中配置信息以 "CELERY_"开头为celery的配置信息
# 自动根据配置查找django的所有子应用下的tasks任务文件
app.autodiscover_tasks()