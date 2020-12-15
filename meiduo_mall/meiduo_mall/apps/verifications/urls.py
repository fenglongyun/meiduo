from django.conf.urls import url
from . import views

urlpatterns = [
    #按短信
    url(r'^sms_code/(?P<mobile>1[3-9]\d{9})/$',views.SMSCodeView.as_view())
]