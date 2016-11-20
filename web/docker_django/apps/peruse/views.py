from django.shortcuts import render, get_object_or_404 # redirect
from .models import Plant, PlantImage
from redis import Redis


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