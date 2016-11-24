from django.shortcuts import render, get_object_or_404 # redirect
from .models import Plant, PlantImage
from redis import Redis
from django.http import HttpResponse
from django.contrib.staticfiles.storage import staticfiles_storage

import requests
import datetime
import time

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
	counter = redis.incr('counter')
	filePath = '/usr/src/app/static/library/xml/dataset-submission-to-OAR.xml'
	MIME = 'application/marcxml+xml'
	OARurl = 'http://oar.sci-gaia.eu/batchuploader/robotupload/insert'
	
	headers = {
		'Content-Type': 'application/marcxml+xml',
		'User-Agent': 'invenio_webupload'
	}

	# now = datetime.datetime.now().strftime('%H:%M:%S')
	seconds = datetime.datetime.now().strftime('%S')
	now = time.mktime(datetime.datetime.now().timetuple())
	doi = str(now).replace(".0", "") + '.' + seconds

	file = open("/usr/src/app/static/library/dois.xml", "w")
	file.write(str(counter) + "\t--\t" + doi  + "\n")
	file.close()

	xmlfile = open(filePath, 'rb')
	files = {'file': (filePath, xmlfile, MIME)}
	# serverResponse = requests.put(OARurl, files=files, headers=headers)
	response = HttpResponse(doi)
	
	return  response