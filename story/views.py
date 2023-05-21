from django.shortcuts import render, redirect, get_object_or_404
from .models import Story, Location, Comment
from accounts.models import Profile
from .forms import WriteStoryForm, EditStoryForm, CommentForm
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

            #Adding tags
            for tag in request.POST.get('tags', '').split(','):
                story.tags.add(tag)

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
    profile = Profile.objects.all()
    new_comment = None

    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.story = story
            new_comment.author = request.user
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'story/read_story.html', {'story': story, 'locations': locations, 'comment_form': comment_form, 'profile':profile})

@login_required
def edit_story(request, story_id):
    if request.user.is_authenticated:
        story = get_object_or_404(Story, id=story_id)
        if request.user == story.owner:
            if request.method == 'POST':
                form = EditStoryForm(request.POST, instance=story)
                if form.is_valid():
                    story = form.save(commit=False)

                    # Remove existing locations
                    story.geolocations.clear()

                    # Add new locations
                    location_data = request.POST.getlist('locations[]')
                    for location in location_data:
                        geolocation_lat, geolocation_lon, description = location.split(',')
                        loc_instance, _ = Location.objects.get_or_create(geolocation_lat=geolocation_lat, geolocation_lon=geolocation_lon, description=description)
                        story.geolocations.add(loc_instance)

                    story.save()
                    return redirect('profile', pk=request.user.id)
            else:
                form = EditStoryForm(instance=story)
            return render(request, 'story/edit_story.html', {'form': form, 'story': story})
        else:
            messages.error(request, "You don't have permission to edit this story.")
            return redirect('profile', pk=request.user.id)
    else:
        messages.error(request, "You are not logged in!")
        return redirect('signInPage')
    
@login_required
def like_story(request, pk):
    story = Story.objects.get(pk=pk)
    if request.user == story.owner:
        messages.error(request, "You can't like your own story!")
    else:
        if request.user in story.likes.all():
            story.likes.remove(request.user)
            messages.success(request, "You removed your like!")
        else:
            story.likes.add(request.user)
            messages.success(request, "You liked this story!")
    return render(request, 'story/read_story.html', {'story': story})