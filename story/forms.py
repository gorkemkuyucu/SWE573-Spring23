from django import forms
from .models import Story, Comment, DateResolution, Season
from django.forms import SelectDateWidget
import calendar

MONTH_CHOICES = [(i, calendar.month_abbr[i]) for i in range(1, 13)]
YEAR_CHOICES = [(i, i) for i in range(1900, 2025)]
DECADE_CHOICES = [(i, i*10) for i in range(190, 203)]
DATE_RESOLUTION_CHOICES = [
    (DateResolution.SINGLE_DATE.value, 'Single Date'),
    (DateResolution.INTERVAL.value, 'Interval'),
    (DateResolution.MONTH.value, 'Month'),
    (DateResolution.YEAR.value, 'Year'),
    (DateResolution.SEASON.value, 'Season'),
    (DateResolution.DECADE.value, 'Decade'),
    ]
SEASON_CHOISES = [
    (None, '-'),
    (Season.WINTER.value, 'Winter'),
    (Season.SPRING.value, 'Spring'),
    (Season.SUMMER.value, 'Summer'),
    (Season.AUTUMN.value, 'Autumn'),
    ]

class WriteStoryForm(forms.ModelForm):
    title = forms.CharField(required=True, label="Title")
    #body = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={"placeholder": "Enter your story here", "class":"form-control",}), label="Here is my story:")
    single_date = forms.DateField(required=False, widget=SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))
    interval_start = forms.DateField(required=False, widget=SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))
    interval_end = forms.DateField(required=False, widget=SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))
    month = forms.IntegerField(required=False)
    year = forms.IntegerField(required=False)
    season = forms.ChoiceField(required=False, choices=SEASON_CHOISES)
    decade = forms.IntegerField(required=False)

    class Meta:
        model = Story
        exclude = ("owner", "is_reported", "likes", "geolocations", "tags" )


class EditStoryForm(forms.ModelForm):
    title = forms.CharField(required=True, label="Title")
    #body = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={"placeholder": "Enter your story here", "class":"form-control",}), label="Here is my story:")
    single_date = forms.DateField(required=False, widget=SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))
    interval_start = forms.DateField(required=False, widget=SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))
    interval_end = forms.DateField(required=False, widget=SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))
    month = forms.IntegerField(required=False)
    year = forms.IntegerField(required=False)
    season = forms.ChoiceField(required=False, choices=SEASON_CHOISES)
    decade = forms.IntegerField(required=False)

    class Meta:
        model = Story
        exclude = ("owner", "is_reported", "likes", "geolocations", "tags" )


class CommentForm(forms.ModelForm):
    text = forms.CharField(required=False, widget=forms.widgets.Textarea(attrs={"placeholder": "Enter your comment here", "class":"form-control",}), label="Here is my comment:")
    
    class Meta:
        model = Comment
        fields = ('text',)
