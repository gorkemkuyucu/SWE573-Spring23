from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.gis.geos import Point
from .forms import MapSearchForm
from .models import MarkedPoint
from story.models import Story, Location
from django.db.models import Q, F, Func
from .forms import AdvancedSearchForm
from django.contrib.auth.models import User
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry
import json
from django.http import JsonResponse
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.db.models.functions import math

# Create your views here.

def map_search(request):
    if request.method == 'POST':
        form = MapSearchForm(request.POST)
        if form.is_valid():
            center_lat = form.cleaned_data.get('latitude')
            center_lon = form.cleaned_data.get('longitude')
            center_point = Point(center_lon, center_lat, srid = 4326)
            radius = form.cleaned_data.get('radius') # Data got in meters, converted into km
            query = 'Drawn location'

            # Calculate the minimum and maximum latitude and longitude values for the circular area
            min_lat, max_lat, min_lon, max_lon = get_bounding_box(center_lat, center_lon, radius)

            # Perform the search query to filter stories within the circular area
            stories = Story.objects.filter(
                locations__geolocation__distance_lte=(center_point, D(m=radius))
            ).annotate(
                distance=Distance('locations__geolocation', center_point)
            )

            return render(request, 'search/results.html', {'stories': stories, 'query': query})

    else:
        form = MapSearchForm()
        return render(request, 'search/map.html', {'form': form})

#Used to convert radius from km to degrees
def get_bounding_box(center_lat, center_lon, radius):
    earth_radius_km = 6371.0  # Earth's radius in kilometers

    # Calculate the latitude and longitude differences for the bounding box
    lat_diff = radius / earth_radius_km * (180 / 3.14159)
    lon_diff = radius / (earth_radius_km * math.Cos(math.Radians(center_lat))) * (180 / 3.14159)

    # Calculate the minimum and maximum latitude and longitude values
    min_lat = center_lat - lat_diff
    max_lat = center_lat + lat_diff
    min_lon = center_lon - lon_diff
    max_lon = center_lon + lon_diff

    return min_lat, max_lat, min_lon, max_lon

def get_geolocation_point(geolocation_lat, geolocation_lon):
    srid = 4326  # SRID for WGS 84 coordinate system

    # Create a Point object with the specified latitude, longitude, and SRID
    point = Point(geolocation_lon, geolocation_lat, srid=srid)
    return point



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
