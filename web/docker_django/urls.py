from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^library/', include('docker_django.apps.peruse.urls')),
	url(r'^', include('docker_django.apps.peruse.urls')),
	url(r'^dashboard/^', include('docker_django.apps.dashboard.urls')),
]
