from django.db import models
from django.contrib.auth.models import AbstractUser
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer, BadData
from django.conf import settings
from meiduo_mall.utils.models import BaseModel

# Create your models here.

class User(AbstractUser):
    """用户模型类"""
    #在Django用户模型类中添加额外字段
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')
    # default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True,
    #                                     on_delete=models.SET_NULL, verbose_name='默认地址')
    class Meta:
        db_table = 'tb_users'  #数据库中的表名
        verbose_name = '用户'
        verbose_name_plural = verbose_name
    

    @staticmethod
    def check_email_token(token):
        """ 写一个User的静态方法，检查解析验证邮箱token，并返回对应的用户对象 """
        #因为不能用用户实例来调用该方法，而是用用户模型类来调用该方法，并返回用户对象，所以需要定义为静态方法
        serializer=TJWSSerializer(settings.SECRET_KEY, 3600*24)
        try:
            user_dict=serializer.loads(token)
        except BadData:
            return None
        else:
            user_id = user_dict.get('id')
            email = user_dict.get('email')
        try:
            user = User.objects.get(id = user_id, email = email)
        except User.DoesNotExist:
            return None

        return user



class Address(BaseModel):
    """用户收货地址"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province_addresses',
                                 verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district_addresses',
                                 verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定电话')
    email = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name='电子邮箱')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')
    default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True,
                                        on_delete=models.SET_NULL, verbose_name='默认地址')