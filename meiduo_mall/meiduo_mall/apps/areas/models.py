from django.db import models

# Create your models here.

class Area(models.Model):
    """ 省区划 自相关表， 外键指向本身 """
    name = models.CharField(max_length= 20, verbose_name='名称')
    parent = models.ForeignKey("self", verbose_name="上级行政区", related_name='subs', null = True, blank= True, on_delete=models.SET_NULL)
    #related_name属性用于指定反向查询的名称  默认值为 一对多的两张表中多的那个表的表名： 表名_set  

    class Meta:
        db_table = 'tb_areas'
        verbose_name = '行政区划'
        verbose_name_plural = '行政区划'
    
    def __str__(self):
        return self.name