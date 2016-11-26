from django import forms
from django.contrib.auth.models import User

from .models import Plant, PlantImage, OARUploadStatus


# class AlbumForm(forms.ModelForm):

#     class Meta:
#         model = Album
#         fields = ['artist', 'album_title', 'genre', 'album_logo']


class PlantInfoForm(forms.ModelForm):

    class Meta:
        model = Plant
        fields = ['plant_name', 'plant_botanical_name', 'plant_order', 'plant_family', 'plant_genus', 'plant_species', 'plant_binomial_name', 'plant_native_name', 'plant_synonyms', 'plant_habitat', 'plant_etymology', 'plant_description', 'plant_cultivation', 'plant_microscopy', 'plant_used_parts', 'plant_uses', 'plant_constituents', 'plant_references', 'plant_author']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
