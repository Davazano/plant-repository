from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404 # redirect
from .models import Plant, PlantImage
from redis import Redis
from django.http import HttpResponse
from .forms import UserForm, PlantInfoForm, PlantImagesForm
from . import helpers

from django.core import serializers

import os

import requests
import datetime
import time

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

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
	form2 = PlantImagesForm(request.POST or None, request.FILES or None)
	plants = Plant.objects.filter(is_visible = True)
	context = { 'form': form, 'form2': form2, 'plants': plants }
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
			context['resp'] = 'Upload of details for ' + str(plantInfo.plant_name) + ' was successful.'
			context['status'] = 'success'
		else:
			context['resp'] = 'Upload of details for ' + str(plantInfo.plant_name) + ' failed.'
			context['status'] = 'fail'
	return render(request, 'library/uploadPlantInfo.html', context)

# def uploadPlantImages(request):
# 	form = PlantImagesForm(request.POST, request.FILES)
# 	context = { "form": form }
# 	fillAuthContext(request, context)
# 	if form.is_valid():
# 		for filename, file in request.FILES.iteritems():
# 			name = request.FILES[filename].name
#     		return HttpResponse(name)
# 		# palntImages = form.save(commit=False)
# 		# palntImages.plant = 'Test image'
# 		# palntImages.image_name = 'Test image'
# 		# palntImages.image_file = request.FILES['album_logo']
# 		# palntImages.image_description = 'Test image'
# 		# palntImages.image_caption = 'Test image'
#   #       # palntImages.user = request.user
#   #       file_type = album.image_file.url.split('.')[-1]
#   #       file_type = file_type.lower()
#   #       if file_type not in IMAGE_FILE_TYPES:
#   #           context = {
#   #               'palntImages': palntImages,
#   #               'form': form,
#   #               'resp': 'Image file must be PNG, JPG, or JPEG',
#   #           }
#   #           return render(request, 'library/uploadPlantInfo.html', context)
#   #       palntImages.save()

#   #       context['resp'] = 'Image uploads were successful.'
# 		# context['status'] = 'success'
#   #       return render(request, 'library/uploadPlantInfo.html', context)
# 		# return HttpResponse("Uploaded")
# 		# request.FILES.get('images')
# 		# return HttpResponse(form)
# 	return HttpResponse("Failed Upload")
# 	# return render(request, 'library/uploadPlantInfo.html', context)

def uploadPlantImages(request):
	form = PlantInfoForm(request.POST or None)
	form2 = PlantImagesForm(request.POST or None, request.FILES or None)
	counter = redis.incr('counter')
	context = {'form': form, 'form2': form2, 'counter': counter}
	fillAuthContext(request, context)
	if form2.is_valid():
		for filename, file in request.FILES.items():
			plantImage = form2.save(commit=False)
			plantImage.plant =  get_object_or_404(Plant, pk = request.POST.get('plant'))
			plantImage.image_name =  request.POST.get('image_name')
			plantImage.image_file =  request.FILES[filename]
			plantImage.image_description =  request.POST.get('image_description')
			plantImage.image_caption = request.POST.get('image_caption')

			if plantImage.save():
				context['resp'] = 'Upload of image for ' + str(plantImage.image_name) + ' was successful.'
				context['status'] = 'success'
			else:
				context['resp'] = 'Upload of image for ' + str(plantImage.image_name) + ' failed.'
				context['status'] = 'fail'
	return render(request, 'library/uploadPlantInfo.html', context)


def PublishPlantInfo(request):
	plants = Plant.objects.all()
	context = { 'plants': plants }
	fillAuthContext(request, context)
	# if request.POST:
	# 	for plantId in request.POST.items():
	# 		if plantId != 'csrfmiddlewaretoken':
	# 			# send plant image to OAR
	# 	return HttpResponse(request.POST)
	return render(request, 'library/publishPlantInfo.html', context)

def fillImageXMLParams(plantImage):
	author = 'David Oguche'
	organisation = 'University of Jos'
	country = 'Nigeria'
	orcid = '0000-0002-5532-8201'
	author2 = 'Ohaeri Uchechukwu'
	organisation2 = 'University of Jos'
	country2 = 'Nigeria'
	orcid2 = '0000-0002-5532-8201'

	keyword = 'Phytomedicinal Plant'
	keyword2 = 'Open Access'
	keyword3 = 'Science Gateway'

	params = {
		'idType' : os.environ['idType'],
		'author' : author,
		'organisation' : organisation,
		'country' : country,
		'orcid' : orcid,
		'imageTitle' : plantImage.image_name,
		'abstract' : plantImage.image_description,
		'licence' : os.environ['license'],
		'licenceUrl' : os.environ['licenseURL'],
		'imageProject' : plantImage.image_caption,
		'author2' : author2,
		'organisation2' : organisation2,
		'country2' : country2,
		'orcid2' : orcid2,
		'curator' : 'CURATOR',
		'doiRef' : '10.15169/sci-gaia:1479297266.09',
		'refTitle': plantImage.image_caption,
		'resProject' : plantImage.image_caption,
		'keyword' : keyword,
		'keyword2' : keyword2,
		'keyword3' : keyword3,
		# 'imageURL' : plantImage.image_file.url,
		'imageURL' : 'https://drive.google.com/file/d/0Bz_VuFzcZVW3cWpzNDVzNnJrdHM/view', # 'http://grid.ct.infn.it/hackfest/example-image.png',
		'imagesUploadCategory' : os.environ['imagesUploadCategory'],
		'language' : 'eng',
		'researchers' : 'Researchers',
		'resType' : 'image'
	}

	return params

def PublishPlantImage(request):
	plantImages = PlantImage.objects.all()
	data = serializers.serialize("json", plantImages, indent=4)
	context = { 'plantImages': plantImages, 'data': data }
	fillAuthContext(request, context)
	if request.POST:
		strV = ""
		for postVar in request.POST.items():
			if postVar[0] != 'csrfmiddlewaretoken':
				plantImg = get_object_or_404(PlantImage, pk = postVar[1])
				XMLparams = fillImageXMLParams(plantImg)
				strV += "<br>" + helpers.sendImageToOAR(XMLparams)
		context['resp'] = 'You have successfully published one or more image(s).'
		context['status'] = 'success'
		return HttpResponse(strV)
		return render(request, 'library/publishPlantImage.html', context)
	return render(request, 'library/publishPlantImage.html', context)