from django.urls import path
from . import views

app_name = 'gameplay'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('stories/', views.StoriesListView.as_view(), name="stories-list"),
    path('stories/new/', views.CreateStoryView.as_view(), name="create-story"),
    path('stories/<int:pk>', views.StoryDetailView.as_view(), name="story-detail"),
]