
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('registration', views.registration_page, name='registration'),
    path('register', views.register, name="register"),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('interview/<str:student_email>/', views.interview, name='interview')
]