from django.urls import path

from .views import character_creation, CharacterSheetView, CharacterListView

urlpatterns = [
    path('create/', character_creation, name='character-create'),
    path('<int:pk>/', CharacterSheetView.as_view(), name='character-sheet'),
    path('all/', CharacterListView.as_view(), name='charactes-list'),
    path('/', CharacterListView.as_view()),
]