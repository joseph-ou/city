'''celery配置文件'''

# 任务队列的链接地址
broker_url = 'redis://127.0.0.1:6379/14'
# 结果队列的链接地址
result_backend = 'redis://127.0.0.1:6379/15'