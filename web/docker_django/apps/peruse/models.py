from django.contrib.auth.models import Permission, User
from django.db import models
from django.conf import settings

class Plant(models.Model):
    user = models.ForeignKey(User, default=1)
    plant_name = models.CharField(max_length = 250, blank = True)
    plant_botanical_name = models.CharField(max_length=250, blank=True)
    plant_order = models.CharField(max_length = 250, blank = True)
    plant_family = models.CharField(max_length = 250, blank = True)
    plant_genus = models.CharField(max_length = 250, blank = True)
    plant_species = models.CharField(max_length = 250, blank = True)

    plant_binomial_name = models.CharField(max_length = 250, blank = True)
    plant_native_name = models.TextField(blank=True)
    plant_synonyms = models.CharField(max_length = 250, blank = True)
    plant_habitat = models.TextField(blank=True)

    plant_etymology = models.TextField(blank = True)
    plant_description = models.TextField(blank = True)
    plant_cultivation = models.TextField(blank = True)
    plant_microscopy = models.TextField(blank=True)

    plant_used_parts = models.CharField(max_length=250, blank=True)
    plant_uses = models.TextField(blank=True)
    plant_constituents = models.TextField(blank=True)
    plant_references = models.TextField(blank=True)
    plant_author = models.CharField(max_length=250, blank=True)

    plant_picture = models.FileField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    is_visible = models.BooleanField(default = False)

    def __str__(self):
        return self.plant_name

class PlantImage(models.Model):
    plant = models.ForeignKey(Plant, on_delete = models.CASCADE)
    image_name = models.CharField(max_length = 250, blank = True)
    image_file = models.FileField()
    image_description = models.TextField(blank = True)
    image_caption = models.CharField(max_length = 250, blank = True)
    is_visible = models.BooleanField(default = False)

    def __str__(self):
        return self.image_name