# from django.shortcuts import render
from  rest_framework.views import APIView
from rest_framework.response import Response
from random import randint
from django_redis import get_redis_connection
import json
import logging
from . import constants
from rest_framework import status
from celery_tasks.sms.tasks import send_sms_code


logger=logging.getLogger('django')

# Create your views here.
class SMSCodeView(APIView):
    """短信验证"""

    def get(self,request,mobile):
        #1. 创建redis连接对象
        redis_conn=get_redis_connection('verify_codes')
        
        #2. 从redis中判断该用户60秒内注册是否请求过获取验证码
        send_flag=redis_conn.get('send_flag_%s' %mobile)
        print(send_flag)
        if send_flag:
            return Response({'message':'验证码请求频繁'},status=status.HTTP_400_BAD_REQUEST)

        #2. 生成验证码
        rand6='%06d' % randint(0,999999)
        sms_code=str(rand6)

        #将验证码写入'django'日志
        logger.info(sms_code)
        
        #3. 把验证码和用户6秒内是否获取过验证码记录存储到redis缓存数据库
        ##创建一个redis管道（对于连续多次操作redis，为了减少连接redis次数，把多个redis操作放到管道中一起执行）
        pl=redis_conn.pipeline()
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        #执行管道
        pl.execute()

        #4. 调用异步任务 利用aliyun云通信发短信
        sms_code_json=json.dumps({'code': sms_code})
        #触发异步任务send_sms_code(mobile,send_code_json)函数
        send_sms_code.delay(mobile,sms_code_json)
        
        #响应
        return Response({'message':'ok'})


