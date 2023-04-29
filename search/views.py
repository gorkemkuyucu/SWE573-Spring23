from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.gis.geos import Point
from .forms import MarkedPointForm
from .models import MarkedPoint

# Create your views here.
def home(request):
    return render(request, 'story/home.html')

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

