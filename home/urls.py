from django.urls import path

from . import views
from .views import *

app_name = "home"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("events/", EventsView.as_view(), name="events"),
    path("officers/", OfficersView.as_view(), name="officers"),
    path("servicehours/", ServiceHoursView.as_view(), name="servicehours"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("signin/", signin, name="signin"),
    path("approve_submission/", approve_submission, name="approve_submission"),

    path("reject_submission/", reject_submission, name="reject_submission"),
]
