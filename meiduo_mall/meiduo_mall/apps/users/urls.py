from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r"^users/$", views.UserView.as_view()),#新增用户接口
    url(r"^users/(?P<username>\w{5,20})/count/$", views.UsernameCountView.as_view()),#判断用户名是否存在
    url(r"^mobiles/(?P<mobile>\d{11,11})/count/$", views.MobileCountView.as_view()),#判断手机号是否已存在
    url(r'^authorizations/', obtain_jwt_token),# 用户登录视图接口
    url(r"^user/$", views.UserDetailView.as_view()), #用户详情接口
    url(r'^email/$',views.EmailView.as_view()),#修改邮箱接口
    url(r'^emails/verification/$',views.VerifyEmailView.as_view()),#激活邮箱接口
]
