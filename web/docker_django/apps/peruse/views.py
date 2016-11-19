from django.shortcuts import render, get_object_or_404 # redirect
from .models import Plant, PlantImage
from redis import Redis


redis = Redis(host='redis', port=6379)

def index(request):
	plants = Plant.objects.filter(is_visible = True)
	counter = redis.incr('counter')
	return render(request, 'library/index.html', {'plants': plants, 'counter': counter})