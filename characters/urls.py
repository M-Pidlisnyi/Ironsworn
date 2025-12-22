from django.urls import path

from .views import character_creation, CharacterSheetView, CharacterListView, AddAssetView

urlpatterns = [
    path('create/', character_creation, name='character-create'),
    path('<int:pk>/', CharacterSheetView.as_view(), name='character-sheet'),
    path('all/', CharacterListView.as_view(), name='charactes-list'),
    path('', CharacterListView.as_view()),
    path('<int:char_id>/add-asset/', AddAssetView.as_view(), name='add-asset'),
]