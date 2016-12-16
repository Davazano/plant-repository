from django.contrib import admin
from .models import Plant, PlantImage, OARUploadStatus, Faqs, Contact, NewsPage

admin.site.register(Plant)
admin.site.register(PlantImage)
admin.site.register(OARUploadStatus)
admin.site.register(Faqs)
admin.site.register(Contact)
admin.site.register(NewsPage)
