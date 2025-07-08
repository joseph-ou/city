'''任务文件 名字必须是tasks.py'''

from ..main import app
from ronglianyunapi import send_sms as send_sms_to_user


@app.task(name='send_sms1')
def send_sms1():
    '''没有任何参数和返回的异步任务'''
    print('<task>:send_sms1 执行')

@app.task(name='send_sms2')
def send_sms2(mobile,code):
    """有参数的异步任务"""
    print(f'<task>:send_sms2 执行 mobile={mobile},code={code} ')


@app.task(name='send_sms3')
def send_sms3():
    """有结果的异步任务"""
    print('<task>:send_sms3 执行 ')
    return 100

@app.task(name='send_sms4')
def send_sms4(x,y):
    '''有参数有结果的任务'''
    print(f"<task>:send_sms4 x={x},y={y} ")
    return x+y


# from ronglianyunapi import send_sms as send_sms_to_user
##正式调用手机短信发送功能

@app.task(name='send_sms')
def send_sms(tid,mobile,datas):
    '''发送短信'''
    print(f"<task>:send_sms tid={tid},mobile={mobile},code={datas} ")

    return send_sms_to_user(tid,mobile,datas)