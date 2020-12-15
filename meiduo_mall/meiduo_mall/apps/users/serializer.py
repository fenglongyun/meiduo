from rest_framework import serializers
from django_redis import get_redis_connection
from .models import User
import re


class CreateUserSerializer(serializers.ModelSerializer):
    """ 注册序列化器"""
    #序列化器的所有字段：['id', 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow']
    #需要校验的字段：['username', 'password', 'password2', 'mobile', 'sms_code', 'allow'] 
    #模型已存在的字段：['id', 'username', 'password', 'mobile']
    
    #需要序列化的字段：['id', 'username', 'mobile']
    #需要反序列化的字段：['username', 'password', 'password2', 'mobile', 'sms_code', 'allow']

    password2=serializers.CharField( label='确认密码', write_only=True)
    sms_code=serializers.CharField(label='验证码', max_length=6, min_length=6, write_only=True)
    allow=serializers.CharField(label='同意协议', write_only=True)  #True
    

    class Meta:
        model=User
        fields=('id', 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow')
        extra_kwargs = {
            # 对模型类中的字段添加规则
            "password":{
                "write_only": True,
                "max_length":20,
                "min_length":8
            },
            "username":{
                "max_length":20,
                "min_length":5
            }
        }



    def validate_mobile(self,value):
        #验证手机号格式
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式有误！')
        return value

    def validate_allow(self,value):
        #验证是否同意协议
        #前端程序员会把true转换成'true'传给后端
        if value != 'true':
            raise serializers.ValidationError('请同意协议')
        return value

    def validate(self, data):
        #验证两次密码是否一致
        if data['password'] != data['password2']:
            raise serializers.ValidationError('两次输入密码不一致')

        redis_conn=get_redis_connection('verify_codes')
        #从redis中拿取验证码
        redis_sms_code=redis_conn.get('sms_%s' % data['mobile'])
        
        if redis_sms_code is None or data['sms_code'] != redis_sms_code.decode():
            raise serializers.ValidationError('验证码已过期')
        return data

    def create(self,validated_data):
        del validated_data['password2']
        del validated_data['allow']
        del validated_data['sms_code']
        print(validated_data)
            
        password=validated_data.pop('password')

        user=User(**validated_data)
        user.set_password(password)
        user.save()
        return user





