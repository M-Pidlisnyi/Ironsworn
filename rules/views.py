from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import AssetDefinition, Move
# Create your views here.
class AssetLibraryView(ListView):
    template_name = 'rules/assets_library.html'
    model = AssetDefinition
    context_object_name = 'assets_list'
    
class MoveReferenceView(ListView):
    template_name = 'rules/move_reference.html'
    model = Move
    context_object_name = 'moves_list'

class MoveDetailView(DetailView):
    model = Move