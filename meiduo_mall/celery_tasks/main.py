from celery import Celery
import os
#读取django配置项，因为celery独立于Django项目运行，默认不能读到django的配置文件，所以需要导入django的配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings.dev')

#1. 创建celery对象
celery_app=Celery('meiduo')

#2. 加载配置文件
celery_app.config_from_object('celery_tasks.config')

#3. 自动注册异步任务
celery_app.autodiscover_tasks(['celery_tasks.sms','celery_tasks.email'])
