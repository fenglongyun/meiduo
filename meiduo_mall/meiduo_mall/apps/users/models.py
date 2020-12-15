from django.db import models
from django.contrib.auth.models import AbstractUser

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

