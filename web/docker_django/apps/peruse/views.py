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
	XMLPath = '/usr/src/app/static/library/xml/'

	templateFile = XMLPath + 'temp/dataset-submission-to-OAR.xml'
	testDir = 'test/'
	XMLPath += testDir
	counter = redis.incr('counter')
	MIME = 'application/marcxml+xml'
	OARurl = 'http://oar.sci-gaia.eu/batchuploader/robotupload/insert'
	
	headers = {
		'Content-Type': 'application/marcxml+xml',
		'User-Agent': 'invenio_webupload'
	}

	# now = datetime.datetime.now().strftime('%H:%M:%S')
	seconds = datetime.datetime.now().strftime('%S')
	now = time.mktime(datetime.datetime.now().timetuple())
	doi = str(now).replace('.0', '') + '.' + seconds

	date = datetime.datetime.now().strftime('%Y-%M-%d')
	author1 = 'Oguche David'
	university1 = 'University of Jos'
	country1 = 'Nigeria'
	number1 = '0000-0002-5532-8201'
	license = 'cc-by-nc-sa'
	licenseURL = 'https://creativecommons.org/licenses/by-nc-sa/3.0/'
	project = 'ACEPRD Plant Repository'
	author2 = 'Ohaeri Uchechukwu'
	university2 = 'University of Jos'
	country2 = 'Nigeria'
	number2 = '0000-0002-5532-8201'
	tag1 = 'ACEPRD'
	tag2 = 'Plant Repository'
	tag3 = 'Open Access'
	datasetFile = 'http://grid.ct.infn.it/hackfest/example-dataset.csv'

	context = {
		'doi' : doi,
		'date' : date,
		'author1' : author1, 
		'university1' : university1,
		'country1' : country1,
		'number1' : number1,
		'license' : license,
		'licenseURL' : licenseURL,
		'project' : project,
		'author2' : author2,
		'university2' : university2,
		'country2' : country2,
		'number2' : number2,
		'tag1' : tag1,
		'tag2' : tag2,
		'tag3' : tag3,
		'datasetFile' : datasetFile	
	}


	file = open(XMLPath + 'dois.txt', 'a')
	file.write(str(counter) + '\t--\t' + doi  + '\n')
	file.close()


	XMLTemplateFile = open(templateFile, 'r')
	XMLStream = XMLTemplateFile.readlines()
	templateStr = ''.join(XMLStream)
	newXMLContentStr = templateStr.format(**context)
	XMLTemplateFile.close()

	XMLFile = XMLPath + doi  + '.xml';

	file = open(XMLFile, 'w')
	file.write(newXMLContentStr)
	file.close()

	file = open(XMLFile, 'rb')

	files = {'file': (XMLFile, file, MIME)}

	serverResponse = requests.put(OARurl, files=files, headers=headers)
	resp = str(newXMLContentStr) + '<br><br>Server Response' + str(serverResponse)
	response = HttpResponse(resp)

	file.close()

	return  response