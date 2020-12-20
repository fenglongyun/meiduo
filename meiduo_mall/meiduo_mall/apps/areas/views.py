#from django.shortcuts import render
from  rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from  rest_framework.response import Response
from rest_framework import status
from .models import Area
from .serializers import AreaListSerializer, AreaDetailSerializer
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.cache.mixins import CacheResponseMixin
# Create your views here.

######### APIVIEW查多个数据list 和 单个数据Retrieve写法
# class AreaListView(APIView):
#     """ 查询所有省 """
#     @cache_response(timeout=60*60, cache='default')   #将响应数据缓存到django缓存，以降低mysql的查询，压力我们之前把django缓存放在redis里，这里设置的是配置文件中default缓存数据库
#     def get(self, request, *args, **kwargs):
#         #获取指定的查询集
#         qs = Area.objects.filter(parent_id =None).all()
#         serializer = AreaListSerializer(qs, many=True)
#         return Response(serializer.data)


# class AreaDetailView(APIView):
#     """ 查询单个行政区，返回它及他的下一级行政区 """
#     @cache_response()
#     def get(self, request, *args, **kwargs):
#         pk=kwargs.get('pk')
#         try:
#             qs = Area.objects.get(id=pk)
#         except Area.DoesNotExist:
#             return Response({'message':'id参数错误'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             serializer = AreaDetailSerializer(qs)
#             return Response(serializer.data)
    



######### Generic写法查多个数据list 和 单个数据Retrieve写法
# class AreaListView(ListAPIView):
#     queryset = Area.objects.filter(parent=None)
#     serializer_class = AreaListSerializer


# class AreaDetailView(RetrieveAPIView):
#     queryset = Area.objects.all()
#     serializer_class = AreaDetailSerializer


class AreaViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """ 将上面两个整合成视图集 """
    #指定序查询集
    def get_queryset(self):
        if self.action == 'list':
            return Area.objects.filter(parent=None)
        else:
            return Area.objects.all()
    #指定序列化器
    def get_serializer_class(self):
        if self.action == 'list':
            return AreaListSerializer
        else: 
            return AreaDetailSerializer
        

        
    