from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.




#Creating user profile
class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)
    about_me = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/Default_profile_picture.svg')
    
    def __str__ (self):
        return self.user.username

@receiver(post_save, sender=User)

#Creating profile when new user is created
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        # making user to follow themselves
        user_profile.follows.set([instance.profile.id])
        user_profile.save()


