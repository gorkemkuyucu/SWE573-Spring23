from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.gis.geos import Point
from .forms import MarkedPointForm
from .models import MarkedPoint
from story.models import Story
from django.db.models import Q
from .forms import AdvancedSearchForm
from django.contrib.auth.models import User

# Create your views here.

def map_view(request):
    if request.method == 'POST':
        form = MarkedPointForm(request.POST)
        if form.is_valid():
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            point = Point(longitude, latitude)
            marked_point = MarkedPoint(location=point)
            marked_point.save()
            return redirect('map')
    else:
        form = MarkedPointForm()
    return render(request, 'search/map.html', {'form': form})




def basic_search(request):
    query = request.GET.get('query')
    stories = []

    if query:
        stories = Story.objects.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(owner__username__icontains=query)
        )

    return render(request, 'search/results.html', {'stories': stories,'query': query})

def advanced_search(request):
    if request.method == 'POST':
        form = AdvancedSearchForm(request.POST)
        if form.is_valid():
            # Get the search parameters from the form
            title = form.cleaned_data.get('title')
            body = form.cleaned_data.get('body')
            author = form.cleaned_data.get('author')
            tags = form.cleaned_data.get('tags')
            date = form.cleaned_data.get('date')
            
            # Filter the Story objects
            stories = Story.objects.all()
            if title:
                stories = stories.filter(title__icontains=title)
                query=title
            if body:
                stories = stories.filter(body__icontains=body)
                query=body
            if author:
                stories = stories.filter(owner__username__icontains=author)
                query=author
            if tags:
                stories = stories.filter(tags__name__in=tags.split())
                query=tags
            if date:
                stories = stories.filter(created_date__date=date)
                query=date

            return render(request, 'search/results.html', {'stories': stories,'query': query})
    else:
        form = AdvancedSearchForm()

    return render(request, 'search/advanced_search.html', {'form': form})
