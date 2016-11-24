from django.shortcuts import render, get_object_or_404 # redirect
from .models import Plant, PlantImage
from redis import Redis
from django.http import HttpResponse
from django.contrib.staticfiles.storage import staticfiles_storage

import requests

redis = Redis(host='redis', port=6379)

def index(request):
	plants = Plant.objects.filter(is_visible = True)
	counter = redis.incr('counter')
	return render(request, 'library/index.html', {'plants': plants, 'counter': counter})

def plant_detail(request, plant_id):
	plant = get_object_or_404(Plant, pk = plant_id)
	plant_images = PlantImage.objects.filter(plant = plant)
	counter = redis.incr('counter')
	return render(request, 'library/detail.html', {'plant': plant, 'plant_images': plant_images, 'counter': counter})

def test(request):
	# filePath = staticfiles_storage.url('library/xml/dataset-submission-to-OAR.xml')
	filePath = '/usr/src/app/static/library/xml/dataset-submission-to-OAR.xml'
	MIME = 'application/marcxml+xml'
	OARurl = 'http://oar.sci-gaia.eu/batchuploader/robotupload/insert'
	
	headers = {
		'Content-Type': 'application/marcxml+xml',
		'User-Agent': 'invenio_webupload'
	}

	xmlfile = open(filePath, 'rb')
	# data = xmlfile.readlines()

	# r = requests.post(OARurl, data=data, headers=headers)
	# r = requests.put(url, data=xmlfile, headers=headers, auth=HTTPDigestAuth("*", "*"))

	files = {'file': (filePath, xmlfile, MIME)}
	serverResponse = requests.put(OARurl, files=files, headers=headers)
	response = HttpResponse(serverResponse)
	# response = HttpResponse(filePath)
	return  response