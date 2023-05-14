from django.urls import path
from . import views

urlpatterns=[
    path('list/', views.list, name="story_list"),
    path('write/', views.write_story, name="write_story"),
    path('read/<int:story_id>/', views.read_story, name="read_story"),
    path('story/edit/<int:story_id>/', views.edit_story, name='edit_story'),
    path('like/<int:pk>/', views.like_story, name='like_story'),
]