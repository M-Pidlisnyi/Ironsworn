from django.shortcuts import render
from django.views.generic import ListView

from .models import AssetDefinition
# Create your views here.
class AssetLibraryView(ListView):
    template_name = 'rules/assets_library.html'
    model = AssetDefinition
    context_object_name = 'assets_list'
    