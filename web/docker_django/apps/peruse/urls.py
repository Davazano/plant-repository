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
	url(r'^dashboard/publish-plant-dataset/', views.PublishPlantDataset, name='dashboard.PublishPlantDataset'),
	url(r'^dashboard/profile-details/', views.researcherProfile, name='dashboard.researcherProfile'),

	# url(r'^q/(?P<plant_id>[0-9]+)/', views.search, name='dashboard.search'),
	url(r'^test/', views.test, name='peruse.test'),
	url(r'^ask/', views.ask, name='peruse.faqs'),
	url(r'^privacy/', views.Privacy, name='peruse.privacy'),
	url(r'^contact-us/', views.contactUs, name='peruse.contact'),
	url(r'^news/', views.news, name='peruse.newsview'),
	url(r'^news-info/(?P<newsPage_id>[0-9]+)/', views.news_detail, name='peruse.news_detail'),
	url(r'^about-us/', views.aboutUs, name='peruse.about'),

	url(r'^search/', views.search, name='peruse.search'),
	url(r'^query/(?P<q>[a-zA-Z0-9_]+)/', views.searchByFirstLetter, name='peruse.searchByFirstLetter'),
	url(r'^test/', views.test, name='peruse.test')

]
