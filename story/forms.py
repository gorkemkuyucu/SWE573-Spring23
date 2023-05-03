from django import forms
from .models import Story

class WriteStoryForm(forms.ModelForm):
    title = forms.CharField(required=True, label="Title")
    body = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={"placeholder": "Enter your story here.", "class":"form-control",}), label="Here is my story:")
    start_date = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={"type":"date"}), label= "In between")
    end_date = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={"type":"date"}), label= "and")



    class Meta:
        model = Story
        exclude = ("owner", "is_reported", "likes", "geolocations" )