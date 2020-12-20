from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import CreateUserSerializer, UserDetailSerializer, EmailSerializer
from .models import User
from rest_framework.permissions import IsAuthenticated



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



class UsernameCountView(APIView):
    """ 判断用户是否存在，存在返回1，不存在返回0 """

    def get(self, request, *args, **kwargs):
        username=kwargs.get('username')
        #查询用户
        count=User.objects.filter(username=username).count()
        #包装返回数据
        data ={
            'username':username,
            'count':count
        }
        return Response(data)


class MobileCountView(APIView):
    """ 判断用户是否存在，存在返回1，不存在返回0 """

    def get(self, request, *args, **kwargs):
        mobile=kwargs.get('mobile')
        #查询手机
        count=User.objects.filter(mobile=mobile).count()
        #包装返回数据
        data ={
            'mobile':mobile,
            'count':count
        }
        return Response(data)


class UserDetailView(RetrieveAPIView):
    """ 指定用户详情序列化器 """
    serializer_class = UserDetailSerializer 

    #指定视图的权限
    permission_classes = [IsAuthenticated]
    

    def get_object(self):
        """ 重写此方法返回，要展示的用户模型对象 """
        return self.request.user
   
    
class EmailView(UpdateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = EmailSerializer


    def get_object(self):
        """ 重写此方法返回，要展示的用户模型对象 """
        return self.request.user


class VerifyEmailView(APIView):
    """ 激活用户邮箱 """
    def get(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        user = User.check_email_token(token)
        if user is None:
            return Response({'message':'激活邮箱失败'},status=status.HTTP_400_BAD_REQUEST)
        user.email_active=True
        user.save()
        return Response({'message':'激活邮箱成功'})
    