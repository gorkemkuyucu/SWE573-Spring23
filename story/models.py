from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Location model to allow multiple locaiton selection
class Location(models.Model):
    geolocation_lat = models.FloatField(null=True, blank=True)
    geolocation_lon = models.FloatField(null=True, blank=True)
    story = models.ForeignKey('Story', related_name="locations", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.story

#Creating story model
class Story(models.Model):
    owner = models.ForeignKey(User, related_name="Stories", null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=5000)
    geolocations = models.ManyToManyField(Location, related_name="story_locations")
    created_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True, blank=True, default=None)
    end_date = models.DateTimeField(null=True, blank=True, default=None)
    is_draft = models.BooleanField(default=True)
    is_reported = models.BooleanField(default=False)
    likes= models.ManyToManyField(User, related_name="like_story", blank=True)
    #reported_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='reported_stories')
    #tags = models.ManyToManyField('Tag')

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