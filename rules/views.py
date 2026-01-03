from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import AssetDefinition, Move
# Create your views here.
class AssetLibraryView(ListView):
    """
    Display the full library of available Ironsworn assets.

    This view presents all :model:`rules.AssetDefinition` entries as a
    browsable reference, allowing players to review and select assets
    for their characters.

    **Template:**
    
    Renders the :template:`rules/assets_library.html` template.

    **Context**

    ``assets_list``
        A queryset of :model:`rules.AssetDefinition` objects is available as ``{{assets_list}}`` context variable
    """
     
    template_name = 'rules/assets_library.html'
    model = AssetDefinition
    context_object_name = 'assets_list'
    
class MoveReferenceView(ListView):
    """
    Display the full reference list of Ironsworn moves.

    This view provides a rules reference for all available
    :model:`rules.Move` definitions, grouped or filtered in the template
    as needed for ease of play.

    **Template:**

    Renders the :template:`rules/move_reference.html` template.
    
    **Context**

    ``moves_list``
        A queryset of :model:`rules.Move` objects is available as ``{{moves_list}}`` context variable
    """
     
    template_name = 'rules/move_reference.html'
    model = Move
    context_object_name = 'moves_list'

class MoveDetailView(DetailView):
    """
    Display detailed rules text for a single Ironsworn move.

    This view presents the trigger, outcomes, and roll type of a single
    :model:`rules.Move` for close reference during play.

    **Template:**
    Renders the :template:`rules/move_detail.html` template.

    **Context**
    
    ``move``
        The instance of :model:`rules.Move` is available as ``{{move}}`` context variable.
    """
    model = Move