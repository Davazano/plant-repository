from django import forms
from django.contrib.auth.models import User

from .models import Plant, PlantImage, PlantDataset, OARUploadStatus, ResearcherProfile


class PlantInfoForm(forms.ModelForm):

    class Meta:
        model = Plant
        fields = ['plant_name', 'plant_botanical_name', 'plant_order', 'plant_family', 'plant_genus', 'plant_species', 'plant_binomial_name', 'plant_native_name', 'plant_synonyms', 'plant_habitat', 'plant_etymology', 'plant_description', 'plant_cultivation', 'plant_microscopy', 'plant_used_parts', 'plant_uses', 'plant_constituents', 'plant_references', 'plant_author']


class PlantImagesForm(forms.ModelForm):

    class Meta:
        model = PlantImage
        fields = ['plant', 'image_name', 'image_file', 'image_description', 'image_caption']


class PlantDatasetsForm(forms.ModelForm):

    class Meta:
        model = PlantDataset
        fields = ['plant', 'dataset_name', 'dataset_file', 'dataset_description']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ResearcherProfileForm(forms.ModelForm):

    class Meta:
        model = ResearcherProfile
        fields = ['fullname', 'organisation', 'country', 'orcid']
