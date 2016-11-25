from django.conf.urls import url
from . import views

app_name = 'peruse'

urlpatterns = [
    url(r'^$', views.index, name='peruse.index'),
	url(r'^(?P<plant_id>[0-9]+)/$', views.plant_detail, name='peruse.plant_detail'),
	url(r'^dashboard/login/$', views.index, name='dashboard.index'),
	url(r'^dashboard/upload-plant-info/', views.uploadPlantInfo, name='dashboard.uploadPlantInfo')
	url(r'^test/', views.test, name='peruse.test')
]
