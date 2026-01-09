from django.urls import path

from .views import (character_creation, CharacterSheetView, CharacterListView, AddAssetView, CharacterAssetsListView, CharacterBondsList,
                    NewBondView, NewVowView)

app_name = 'characters'

urlpatterns = [
    path('create/', character_creation, name='character-create'),
    path('<int:pk>/', CharacterSheetView.as_view(), name='character-sheet'),
    path('all/', CharacterListView.as_view(), name='charactes-list'),
    path('', CharacterListView.as_view()),
    path('<int:char_id>/add-asset/', AddAssetView.as_view(), name='add-asset'),
    path('<int:char_id>/assets/', CharacterAssetsListView.as_view(), name='character-assets-list'),
    path('<int:char_id>/bonds/', CharacterBondsList.as_view(), name='character-bonds-list'),
    path('<int:char_id>/add-bond/', NewBondView.as_view(), name='add-bond'),
    path('<int:char_id>/add-vow/', NewVowView.as_view(), name='add-vow'),
]