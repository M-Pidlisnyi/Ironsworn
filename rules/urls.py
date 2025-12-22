from django.urls import path

from .views import AssetLibraryView

urlpatterns = [
    path('library/', AssetLibraryView.as_view(), name='assets-library')
]