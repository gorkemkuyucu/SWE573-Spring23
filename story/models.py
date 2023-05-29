from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from django.contrib.gis.db.models import PointField

# Create your models here.

#Location model to allow multiple locaiton selection
class Location(models.Model):
    geolocation = PointField(null=True, blank=True)
    story = models.ForeignKey('Story', related_name="locations", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.story)


class DateResolution(models.TextChoices):
    SINGLE_DATE = 'single_date'
    INTERVAL = 'interval'
    MONTH = 'month'
    YEAR = 'year'
    SEASON = 'season'
    DECADE = 'decade'

class Season(models.TextChoices):
    WINTER = 'WINTER', 'Winter'
    SPRING = 'SPRING', 'Spring'
    SUMMER = 'SUMMER', 'Summer'
    AUTUMN = 'AUTUMN', 'Autumn'


#Creating story model
class Story(models.Model):
    owner = models.ForeignKey(User, related_name="Stories", null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    body = RichTextField(blank=True, null=True)
    geolocations = models.ManyToManyField(Location, related_name="story_locations")
    created_date = models.DateTimeField(auto_now_add=True)
    is_draft = models.BooleanField(default=True)
    is_reported = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name="like_story", blank=True)
    #reported_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='reported_stories')
    tags = TaggableManager('Tag', blank=True)

    #Adding date resolution
    single_date = models.DateField(null=True, blank=True, default=None)
    interval_start = models.DateField(null=True, blank=True, default=None)
    interval_end = models.DateField(null=True, blank=True, default=None)
    month = models.PositiveIntegerField(null=True, blank=True, default=None)
    year = models.PositiveIntegerField(null=True, blank=True, default=None)
    season = models.CharField(max_length=10,choices=Season.choices, null=True, blank=True, default=None)
    decade = models.PositiveIntegerField(null=True, blank=True, default=None)
    date_resolution = models.CharField(max_length=20, choices=DateResolution.choices, default=DateResolution.SINGLE_DATE,)

    # Count likes
    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return(
            f"{self.owner}"
            f"({self.title})"
            f"({self.body})"
            f"({self.created_date:%Y-%m-%d}):"            
            )

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)

class Comment(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=2000)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
