from django.urls import path

from .views import AssetLibraryView, MoveReferenceView, MoveDetailView

urlpatterns = [
    path('library/', AssetLibraryView.as_view(), name='assets-library'),
    path('moves/', MoveReferenceView.as_view(), name='move-reference'),
    path('moves/<int:pk>/', MoveDetailView.as_view(), name='move-detail'),
]