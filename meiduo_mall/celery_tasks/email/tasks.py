from django.core.mail import send_mail
from celery_tasks.main import celery_app
from django.conf import settings

@celery_app.task(name='sendemail')
def sendemail(to_email, verify_url):
    """ 
    to_email:收件人邮箱；
    verify_url:验证链接地址；
    """
    subject = '美多商城邮箱验证'#邮件主题
    message = ''#邮件正文
    from_email = settings.EMAIL_FROM #读取django配置文件中邮件来源
    recipient_list = [to_email]
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)
    send=send_mail(subject, message, from_email, recipient_list, html_message=html_message)
