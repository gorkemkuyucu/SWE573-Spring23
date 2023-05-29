from django import forms
from django.contrib.auth.models import User
from story.models import Story, Season

SEASON_CHOISES = [    
    (None, '-'),
    (Season.WINTER.value, 'Winter'),
    (Season.SPRING.value, 'Spring'),
    (Season.SUMMER.value, 'Summer'),
    (Season.AUTUMN.value, 'Autumn'),
    ]

class MapSearchForm(forms.Form):
    latitude = forms.FloatField()
    longitude = forms.FloatField()
    radius = forms.FloatField()

class AdvancedSearchForm(forms.Form):
    title = forms.CharField(required=False)
    body = forms.CharField(required=False)
    author = forms.CharField(required=False)
    tags = forms.CharField(required=False)
    created_date = forms.DateField(required=False)
    season = forms.ChoiceField(required=False, choices=SEASON_CHOISES)