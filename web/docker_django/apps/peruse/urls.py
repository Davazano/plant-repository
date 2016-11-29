from django.conf.urls import url
from . import views

app_name = 'peruse'

urlpatterns = [
    url(r'^$', views.index, name='peruse.index'),
	url(r'^plant-info/(?P<plant_id>[0-9]+)/$', views.plant_detail, name='peruse.plant_detail'),
	url(r'^dashboard/login/$', views.signin, name='dashboard.signin'),
	url(r'^dashboard/logout_user/$', views.logout_user, name='dashboard.logout_user'),
	url(r'^dashboard/upload-plant-info/', views.uploadPlantInfo, name='dashboard.uploadPlantInfo'),
	url(r'^dashboard/upload-plant-images/', views.uploadPlantImages, name='dashboard.uploadPlantImages'),
	url(r'^dashboard/upload-plant-datasets/', views.uploadPlantDatasets, name='dashboard.uploadPlantDatasets'),
	url(r'^dashboard/publish-plant/', views.PublishPlantInfo, name='dashboard.PublishPlantInfo'),
	url(r'^dashboard/publish-plant-image/', views.PublishPlantImage, name='dashboard.PublishPlantImage'),
	url(r'^dashboard/profile-details/', views.researcherProfile, name='dashboard.researcherProfile'),
	url(r'^test/', views.test, name='peruse.test')
]
