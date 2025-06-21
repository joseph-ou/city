'''自定义引入容联云短信功能实现登录'''

import json
from ronglian_sms_sdk import SmsSDK
from django.conf import settings

def send_sms(tid,mobile,datas):
    '''发送短信
    params: tid:模板id 测试用默认为1 商用要在平台自定义
    params: mobile: 接收短信的手机号，多个手机号用逗号隔开 多个号码：mobile:"133xxxxxxxx,133xxxxxxxxx"
    params: datas: 短信模板对应要的参数
    '''

    ronglianyun=settings.RONGLIANYUN
    sdk=SmsSDK(ronglianyun.get('accId'),ronglianyun.get('accToken'),ronglianyun.get('appId'))

    resp=sdk.sendMessage(tid,mobile,datas)

    res=json.loads(resp)
    # print(res,type(res))
    return res.get('statuscode')== '000000'