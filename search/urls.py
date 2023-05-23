from django.urls import path
from . import views

urlpatterns=[
    path('map/', views.map_search, name="map"),
    path('basic/', views.basic_search, name="basic_search"),
    path('advanced/', views.advanced_search, name="advanced_search"),

]