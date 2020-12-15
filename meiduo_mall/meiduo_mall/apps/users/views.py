from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import CreateUserSerializer


# Create your views here.
#创建用户可以用以下两种方法
# 1. 继承GenericAPIView
# class UserView(GenericAPIView):
#     serializer_class=CreateUserSerializer
    
#     def post(self,request):
        
#         ser=self.get_serializer(data=request.data)
#         ser.is_valid(raise_execption=True)
#         ser.save()
#         return Response(ser.data,status=status.HTTP_201_CREATED)

# 2. 继承GenericAPIView
class UserView(CreateAPIView):
    serializer_class=CreateUserSerializer
