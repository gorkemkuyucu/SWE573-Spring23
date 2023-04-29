from django import forms

class MarkedPointForm(forms.Form):
    latitude = forms.FloatField()
    longitude = forms.FloatField()