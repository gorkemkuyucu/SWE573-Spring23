from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name="home"),
    path('sign_up/', views.signUpPage, name="signUpPage"),
    path('sign_up/terms_conditions/', views.termsConditions, name="termsConditions"),
    path('verification/', views.verification, name='verification'),
    path('sign_in/', views.signInPage, name="signInPage"),
    path('profiles/', views.profile_list, name='profiles'),
    path('profiles/<int:pk>', views.profile, name='profile'),
]