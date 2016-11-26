from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404 # redirect
from .models import Plant, PlantImage
from redis import Redis
from django.http import HttpResponse
from .forms import UserForm, PlantInfoForm
from . import helpers

import requests
import datetime
import time

redis = Redis(host='redis', port=6379)

def index(request):
	plants = Plant.objects.filter(is_visible = True)
	counter = redis.incr('counter')
	context = {'plants': plants, 'counter': counter}
	fillAuthContext(request, context)
	return render(request, 'library/index.html', context)

def plant_detail(request, plant_id):
	plant = get_object_or_404(Plant, pk = plant_id)
	plant_images = PlantImage.objects.filter(plant = plant)
	counter = redis.incr('counter')
	context = {'plant': plant, 'plant_images': plant_images, 'counter': counter}
	fillAuthContext(request, context)
	return render(request, 'library/detail.html', context)

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

# def signin(request):
# 	return render(request, 'library/login.html')

def fillAuthContext(request, context):
	context['authenticated'] = request.user.is_authenticated()
	if context['authenticated'] == True:
		context['username'] = request.user.username

	return HttpResponse(context)

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # albums = Album.objects.filter(user=request.user)
                fillAuthContext(request, context)
                return render(request, 'library/index.html', context)
    context = {
        "form": form,
    }
    return render(request, 'library/register.html', context)

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # albums = Album.objects.filter(user=request.user)
                context = {}
                fillAuthContext(request, context)
                return render(request, 'library/index.html', context)
                # return render(request, 'library/index.html', userContext)
            else:
                return render(request, 'library/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'library/login.html', {'error_message': 'Invalid Credentials'})
    return render(request, 'library/login.html')

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'library/login.html', context)

def uploadPlantInfo(request):
	form = PlantInfoForm(request.POST or None)
	context = { "form": form }
	fillAuthContext(request, context)
	if form.is_valid():
		plantInfo = form.save(commit=False)
		plantInfo.plant_name = request.POST.get('plant_name')
		plantInfo.plant_botanical_name = request.POST.get('plant_botanical_name')
		plantInfo.plant_order = request.POST.get('plant_order')
		plantInfo.plant_family = request.POST.get('plant_family')
		plantInfo.plant_genus = request.POST.get('plant_genus')
		plantInfo.plant_species = request.POST.get('plant_species')
		plantInfo.plant_binomial_name = request.POST.get('plant_binomial_name')
		plantInfo.plant_native_name = request.POST.get('plant_native_name')
		plantInfo.plant_synonyms = request.POST.get('plant_synonyms')
		plantInfo.plant_habitat = request.POST.get('plant_habitat')
		plantInfo.plant_etymology = request.POST.get('plant_etymology')
		plantInfo.plant_description = request.POST.get('plant_description')
		plantInfo.plant_cultivation = request.POST.get('plant_cultivation')
		plantInfo.plant_microscopy = request.POST.get('plant_microscopy')
		plantInfo.plant_used_parts = request.POST.get('plant_used_parts')
		plantInfo.plant_uses = request.POST.get('plant_uses')
		plantInfo.plant_constituents = request.POST.get('plant_constituents')
		plantInfo.plant_references = request.POST.get('plant_references')
		# plantInfo.plant_author = request.POST.get('plant_author')
		plantInfo.is_visible = True
		plantInfo.user = request.user
		if plantInfo.save():
			context['resp'] = 'Upload of details for ' + str(plantInfo.plant_name) + 'was successful.'
			context['status'] = 'success'
		else:
			context['resp'] = 'Upload of details for ' + str(plantInfo.plant_name) + 'failed.'
			context['status'] = 'fail'
		return render(request, 'library/detail.html', {'plantInfo': plantInfo})
	return render(request, 'library/uploadPlantInfo.html', context)
