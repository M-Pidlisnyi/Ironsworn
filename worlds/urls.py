from django.urls import path
from django.views.generic import DetailView, ListView

from .models import World

app_name = "worlds"
urlpatterns = [
    path("all/", ListView.as_view(model=World), name="worlds-list"),
    path("<int:pk>", DetailView.as_view(model=World), name="world-detail"),
]