from django.contrib import admin
from .models import Plant, PlantImage, OARUploadStatus

admin.site.register(Plant)
admin.site.register(PlantImage)
admin.site.register(OARUploadStatus)
