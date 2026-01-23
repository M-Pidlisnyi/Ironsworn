from django.urls import path

from . import views

app_name = 'characters'

urlpatterns = [
    path('create/', views.character_creation, name='character-create'),
    path('<int:pk>/', views.CharacterSheetView.as_view(), name='character-sheet'),
    path('all/', views.CharacterListView.as_view(), name='charactes-list'),
    path('', views.CharacterListView.as_view()),
    path('<int:char_id>/add-asset/', views.AddAssetView.as_view(), name='add-asset'),
    path('<int:char_id>/assets/', views.CharacterAssetsListView.as_view(), name='character-assets-list'),
    path('<int:char_id>/bonds/', views.CharacterBondsList.as_view(), name='character-bonds-list'),
    path('<int:char_id>/bond/<int:pk>/edit/', views.EditBondView.as_view(), name='edit-bond'),
    path('<int:char_id>/add-bond/', views.NewBondView.as_view(), name='add-bond'),
    path('<int:char_id>/add-vow/', views.NewVowView.as_view(), name='add-vow'),
    path('<int:char_id>/quests/', views.MinorQuestsListView.as_view(), name='quests-list'),
    path('<int:char_id>/asset/<int:pk>/edit', views.CharacterAssetEditView.as_view(), name='character-asset-edit'),
    path('<int:char_id>/quest/add', views.NewMinorQuestView.as_view(), name="add-quest"),
    path('<int:char_id>/vows/', views.CharacterVowsListView.as_view(), name="vows-list"),
    path('<int:char_id>/vow/<int:pk>/edit/', views.EditVowView.as_view(), name="edit-vow"),
    path('<int:char_id>/change/', views.change_resource, name="change-resource"),
    path('<int:char_id>/progress', views.increase_progress, name="increase-progress"),
]