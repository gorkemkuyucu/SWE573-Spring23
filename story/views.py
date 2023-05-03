from django.shortcuts import render, redirect, get_object_or_404
from.models import Story, Location
from.forms import WriteStoryForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

# Create your views here.

def list(request):
    stories = Story.objects.all().order_by("-created_date")
    return render(request, 'story/list.html', {"stories":stories})
    
@login_required
def write_story(request):
    
    if request.method == 'POST': 
        story_form = WriteStoryForm(request.POST)
        if story_form.is_valid():
            story = story_form.save(commit=False)
            story.owner = request.user
            story.save()

            # Process the story_locations input
            story_locations = request.POST.get('story_locations', '')
            if story_locations:
                locations = story_locations.split('|')
                for location in locations:
                    lat, lon = location.split(',')
                    loc = Location(geolocation_lat=float(lat), geolocation_lon=float(lon), story=story)
                    loc.save()
                    story.geolocations.add(loc)


            messages.success(request, f'Your story has been created successfully!')
            return redirect('story_list')
        else:
            messages.error(request, 'Form is not valid, please try again!')
    else:
        story_form = WriteStoryForm()

    return render(request, 'story/write_story.html', {'story_form': story_form})


def read_story(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    locations = story.geolocations.all()
    return render(request, 'story/read_story.html', {'story': story, 'locations': locations})