from django.shortcuts import render, get_object_or_404 # redirect
from .models import Plant, PlantImage
from redis import Redis
from django.http import HttpResponse

redis = Redis(host='redis', port=6379)

def index(request):
	return render(request, 'dashboard/login.html')

def uploadPlantInfo(request, plant_id):
	counter = redis.incr('counter')
	return render(request, 'dashboard/uploadPlantInfo.html', {'counter': counter})
