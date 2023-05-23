from django import forms
from django.contrib.auth.models import User
from story.models import Story

class MapSearchForm(forms.Form):
    latitude = forms.FloatField()
    longitude = forms.FloatField()
    radius = forms.FloatField()

class AdvancedSearchForm(forms.Form):
    title = forms.CharField(required=False)
    body = forms.CharField(required=False)
    author = forms.CharField(required=False)
    tags = forms.CharField(required=False)
    date = forms.DateField(required=False)