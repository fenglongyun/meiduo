from rest_framework import serializers
from .models import Area


class AreaListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = ['id', 'name']



class AreaDetailSerializer(serializers.ModelSerializer):

    subs = AreaListSerializer(many=True)  #嵌套序列化器
    # subs = serializers.PrimaryKeyRelatedField()   返回多表中的关联id
    # subs = serializers.StringRelatedField()       返回多表中关联模型对象的string方法 在模型类中的def __str__(self)方法中指定

    class Meta:
        model = Area
        fields = ['id', 'name', 'subs']