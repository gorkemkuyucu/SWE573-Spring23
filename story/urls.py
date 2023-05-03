from django.urls import path
from . import views

urlpatterns=[
    path('list/', views.list, name="story_list"),
    path('write/', views.write_story, name="write_story"),
    path('read/<int:story_id>/', views.read_story, name="read_story"),
]