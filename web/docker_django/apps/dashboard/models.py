from django.db import models
from docker_django.apps.peruse.models import Plant, PlantImage

class OARUploadStatus(models.Model):
    doi = models.CharField(max_length = 250)
    status = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    is_visible = models.BooleanField(default = False)

    def __str__(self):
        return self.doi