#1.导入celery类
import os,django
from celery import Celery

app=Celery('city')
#初始化django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','luffycityapi.settings.dev' )
django.setup()#使用脚本对django实现orm操作时一定要进行该步骤


#2.加载配置
app.config_from_object('mycelery.settings')#从配置文件中加载配置


#3.注册任务
# 自动搜索并加载任务
# 参数必须必须是一个列表，里面的每一个任务都是任务的路径名称
# app.autodiscover_tasks(["任务1","任务2",....])
app.autodiscover_tasks(["mycelery.sms","mycelery.mail"])


#4.启动celery
# 强烈建议切换目录到项目的根目录下启动celery!!
#cd 根目录
# celery -A mycelery.main worker --loglevel=info

#5.在终端下调用异步任务或者在其他任务下调动异步任务