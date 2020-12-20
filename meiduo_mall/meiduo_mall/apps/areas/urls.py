from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    #url(r'^areas/$', views.AreaListView.as_view()), #获取一级行政区列表
    #url(r'^areas/(?P<pk>\d+)/$', views.AreaDetailView.as_view()), #根据行政区id获取它的下一级行政区列表
]

router = DefaultRouter()
router.register(r'^areas', views.AreaViewSet, basename='area') #行政区查询集
urlpatterns += router.urls