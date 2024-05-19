from django.urls import path

from . import views
from .views import *

app_name = "home"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("events/", EventsView.as_view(), name="events"),
    path("officers/", OfficersView.as_view(), name="officers"),
    path("profile/", profile, name="profile"),
    path("signin/", signin, name="signin"),
]