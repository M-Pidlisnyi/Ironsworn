from django.urls import path
from django.views.generic import DetailView, ListView

from .models import World
from .views import NewWorldView, set_wordlTruths

app_name = "worlds"
urlpatterns = [
    path("all/", ListView.as_view(model=World), name="worlds-list"),
    path("<int:pk>", DetailView.as_view(model=World), name="world-detail"),
    path("create/", NewWorldView.as_view(), name='world-create'),
    path("<int:pk>/truths/", set_wordlTruths, name="set-truths")
]