from django.shortcuts import render, redirect, get_object_or_404
from .models import Story, Location, Comment, DateResolution
from accounts.models import Profile
from .forms import WriteStoryForm, EditStoryForm, CommentForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.gis.geos import Point

# Create your views here.

def list(request):
    stories = Story.objects.all().order_by("-created_date")
    return render(request, 'story/list.html', {"stories":stories})
    
@login_required(login_url='signInPage')
def write_story(request):
    
    if request.method == 'POST': 
        story_form = WriteStoryForm(request.POST)
        if story_form.is_valid():
            story = story_form.save(commit=False)
            story.owner = request.user
            
            date_resolution = story_form.cleaned_data['date_resolution']
            story.date_resolution = date_resolution
            # process dates
            if date_resolution == DateResolution.SINGLE_DATE:
                single_date = story_form.cleaned_data['single_date']
                if single_date:
                    story.single_date = single_date
                else:
                    messages.error(request, "You should select a date!")
                    return redirect('write_story')
            elif date_resolution == DateResolution.INTERVAL:
                start_date = story_form.cleaned_data['interval_start']
                end_date = story_form.cleaned_data['interval_end']
                if start_date and end_date:
                    story.interval_start = start_date
                    story.interval_end = end_date
                else:
                    messages.error(request, "You should select both dates!")
                    return redirect('write_story')
            elif date_resolution == DateResolution.MONTH:
                month = story_form.cleaned_data['month']
                if month:
                    story.month = month
                else:
                    messages.error(request, "You should select a month!")
                    return redirect('write_story')
            elif date_resolution == DateResolution.YEAR:
                year = story_form.cleaned_data['year']
                if year:
                    story.year = year
                else:
                    messages.error(request, "You should select a year!")
                    return redirect('write_story')
            elif date_resolution == DateResolution.SEASON:
                season = story_form.cleaned_data['season']
                if season:
                    story.season = season
                else:
                    messages.error(request, "You should select a season!")
                    return redirect('write_story')
            elif date_resolution == DateResolution.DECADE:
                decade = story_form.cleaned_data['decade']
                if decade:
                    story.decade = decade
                else:
                    messages.error(request, "You should select a decade!")
                    return redirect('write_story')
            
            story_locations = request.POST.get('story_locations', '')
            if story_locations:
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
                        point = Point(float(lon), float(lat))
                        loc = Location(geolocation=point, story=story)
                        loc.save()
                        story.geolocations.add(loc)


                messages.success(request, f'Your story has been created successfully!')
                return redirect('story_list')
            else:
               messages.error(request, "You should add at least one location!") 
        else:
            messages.error(request, 'Form is not valid, please try again!')
            print(story_form.errors) #debugging
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

@login_required(login_url='signInPage') 
@login_required(login_url='signInPage')
def edit_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    
    if request.user != story.owner:
        messages.error(request, "You don't have permission to edit this story.")
        return redirect('profile', pk=request.user.id)

    if request.method == 'POST':
        form = EditStoryForm(request.POST, instance=story)
        if form.is_valid():
            story = form.save(commit=False)
            
            date_resolution = form.cleaned_data['date_resolution']
            story.date_resolution = date_resolution

            if date_resolution == DateResolution.SINGLE_DATE:
                single_date = form.cleaned_data['single_date']
                if not single_date:
                    messages.error(request, "You should select a date!")
                    return redirect('edit_story', story_id=story_id)
                story.single_date = single_date
            elif date_resolution == DateResolution.INTERVAL:
                start_date = form.cleaned_data['interval_start']
                end_date = form.cleaned_data['interval_end']
                if not start_date or not end_date:
                    messages.error(request, "You should select both dates!")
                    return redirect('edit_story', story_id=story_id)
                story.interval_start = start_date
                story.interval_end = end_date
            elif date_resolution == DateResolution.MONTH:
                month = form.cleaned_data['month']
                if not month:
                    messages.error(request, "You should select a month!")
                    return redirect('edit_story', story_id=story_id)
                story.month = month
            elif date_resolution == DateResolution.YEAR:
                year = form.cleaned_data['year']
                if not year:
                    messages.error(request, "You should select a year!")
                    return redirect('edit_story', story_id=story_id)
                story.year = year
            elif date_resolution == DateResolution.SEASON:
                season = form.cleaned_data['season']
                if not season:
                    messages.error(request, "You should select a season!")
                    return redirect('edit_story', story_id=story_id)
                story.season = season
            elif date_resolution == DateResolution.DECADE:
                decade = form.cleaned_data['decade']
                if not decade:
                    messages.error(request, "You should select a decade!")
                    return redirect('edit_story', story_id=story_id)
                story.decade = decade

            story_locations = request.POST.get('story_locations', '')
            if not story_locations:
                messages.error(request, "You should add at least one location!")
                return redirect('edit_story', story_id=story_id)

            # Remove existing locations
            story.geolocations.clear()

            # Add new locations
            location_data = request.POST.getlist('locations[]')
            for location in location_data:
                geolocation_lat, geolocation_lon, description = location.split(',')
                point = Point(float(geolocation_lon), float(geolocation_lat))
                loc_instance, _ = Location.objects.get_or_create(geolocation=point, description=description)
                story.geolocations.add(loc_instance)

            # Save the story
            story.save()

            # Adding tags
            tags = request.POST.get('tags', '').split(',')
            story.tags.set(tags)

            messages.success(request, 'Your story has been edited successfully!')
            return redirect('profile', pk=request.user.id)
        else:
            messages.error(request, 'Form is not valid, please try again!')
    else:
        form = EditStoryForm(instance=story)

    return render(request, 'story/edit_story.html', {'form': form, 'story': story})

    
@login_required(login_url='signInPage') 
def like_story(request, pk):
    story = Story.objects.get(pk=pk)
    if request.user == story.owner:
        messages.error(request, "You can't like your own story!")
    else:
        if request.user in story.likes.all():
            story.likes.remove(request.user)
            messages.success(request, "You removed your like!")
            return redirect('read_story', pk)
        else:
            story.likes.add(request.user)
            messages.success(request, "You liked this story!")
            return redirect('read_story', pk)
    return render(request, 'story/read_story.html', {'story': story})