from django.contrib.auth.backends import ModelBackend
from .models import User
import re




def jwt_response_payload_handler(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.

    Example:

    def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }

    """
    #重写jwt登录视图的响应数据函数，增加响应数据user.id , user.username 给前端
    #传入参数user 为验证过后的用户模型对象
    print('xxxxx')
    return {
        'token': token,
        'user_id':user.id,
        'username':user.username
    }




def get_user_by_account(account):
    """ 通过用户名或密码获取user模型对象 """
    #获取到返回user对象，获取不到返回None
    try:
        if re.match(r'^1[3-9]\d{9}$',account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user



class UsernameMobileAuthBackend(ModelBackend):


    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        if user and user.check_password(password):
            return user
        
        

    



