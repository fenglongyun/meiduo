from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from celery_tasks.main import celery_app
import time

@celery_app.task(name='send_sms_code')
def send_sms_code(mobile,sms_code_json):
    #time.sleep(5)
    client = AcsClient('LTAI4G6iT2QPTJ1aJ4tnmKUs', '7y9lg6jWcHfa6g6IA4lr5ty9uKL7wl', 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', mobile)
    request.add_query_param('SignName', "冯的商城")
    request.add_query_param('TemplateCode', "SMS_206746842")
    request.add_query_param('TemplateParam', sms_code_json)
    
    #执行发送短信
    #response = client.do_action(request)
    response=sms_code_json
    # python2:  print(response) 
    print(response)