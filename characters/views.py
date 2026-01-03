from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, ListView
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required

from rules.models import AssetDefinition

from .models import Character, Bond, Vow, CharacterAsset
from .forms import CharBaseInfoForm, CharStatsForm, CharResoursesForm, CharInitialBondsForm, BackgroungVowForm, CharacterAssetForm, InitialAssetsForm

CC_STAGES_FORMS = [
    CharBaseInfoForm,
    CharStatsForm,
    CharResoursesForm,
    CharInitialBondsForm,
    BackgroungVowForm,
    InitialAssetsForm,
]

@login_required
def character_creation(request: HttpRequest):
    try:
        stage = int(request.GET.get('stage', 1))
    except ValueError:
        stage = 1
    if stage < 1 or stage > len(CC_STAGES_FORMS):
        stage = 1 

    form_class = CC_STAGES_FORMS[stage - 1]

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            # Save form data to session
            if 'char_creation_data' not in request.session:
                request.session['char_creation_data'] = {}
            request.session['char_creation_data'].update(form.cleaned_data)
            request.session.modified = True
           
            if stage < len(CC_STAGES_FORMS):
                return redirect(request.path + f'?stage={stage+1}')
            else:
                #save_character gets data from session and creates Character object
                
                return save_character(request)
    else:
        form = form_class()

    return render(request, 'characters/character_creation.html', {'form': form})

def save_character(request: HttpRequest) -> HttpResponse:
    data:dict = request.session.get('char_creation_data', {})
    
    # Extract bond descriptions from data (they shouldn't be saved to Character model)
    bond_descriptions:list[str] = [
        data.pop('bond_description_1', ''),
        data.pop('bond_description_2', ''),
        data.pop('bond_description_3', ''),
    ]
    
    # Extract vow data
    vow_description:str = data.pop('vow_description', '')
    vow_difficulty = data.pop('difficulty', 0)
 
    #Extract assets data
    initial_assets = [
        data.pop('asset_definition_1', None),
        data.pop('asset_definition_2', None),
        data.pop('asset_definition_3', None),
    ]

    character = Character.objects.create(user=request.user, **data)

    # Create Bond objects for non-empty descriptions
    for description in bond_descriptions:
        if description.strip():
            Bond.objects.create(character=character, description=description)
    
    # Create Vow with progress set to 0
    if vow_description:
        Vow.objects.create(
            character=character,
            description=vow_description,
            difficulty=vow_difficulty,
            progress=0
        )

    # Create CharacterAsset objects for selected assets
    for asset_def_id in initial_assets:
        if asset_def_id:
            try:
                asset_definition = AssetDefinition.objects.get(id=asset_def_id)
                CharacterAsset.objects.create(
                    character=character,
                    definition=asset_definition
                )
            except AssetDefinition.DoesNotExist:
                continue  # Skip invalid asset definitions

    del request.session['char_creation_data']
    return redirect('character-sheet', pk=character.pk)

class CharacterSheetView(DetailView):
    model = Character
    template_name = 'characters/character_sheet.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context  = super().get_context_data(**kwargs)
        context["momentum_tracker"] = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5, -6]
        context["difficulty_tracker"] = ["troublesome","dangerous","formidable","extreme","epic"]
        character:Character = self.get_object() # type: ignore
        context["statuses"] = [
            ("HEALTH", character.health),
            ("SPIRIT", character.spirit),
            ("SUPPLY", character.supply)
        ]
        context["status_tracker"] = [5, 4, 3, 2, 1]

        context["conditions_list"] = ["wounded", "shaken", "unprepared", "encumbered"]
        context["char_conditions"] = [d.name for d in self.get_object().debilities.filter(type="cond")] # type: ignore

        context["banes_list"] = ["maimed", "corrupted"]
        context["char_banes"] = [d.name for d in self.get_object().debilities.filter(type="bane")]# type: ignore

        context["burdens_list"] = ["cursed", "tormented"]
        context["char_burdens"] = [d.name for d in self.get_object().debilities.filter(type="burd")]# type: ignore


        return context

class CharacterListView(ListView):
    model = Character

    def get_queryset(self):
        return Character.objects.filter(user=self.request.user)
    
class AddAssetView(CreateView):
    model = CharacterAsset
    template_name = 'characters/add_asset.html'
    form_class = CharacterAssetForm

    def form_valid(self, form):
        obj = form.save(commit=False)

        character_id = self.kwargs.get('char_id')
        character = Character.objects.get(id=character_id)

        obj.character = character
        obj.save()
        return redirect('character-sheet', pk=character_id)

class CharacterAssetsListView(ListView):
    model = CharacterAsset
    context_object_name = 'assets_list'

    def get_queryset(self):
        character_id = self.kwargs.get('char_id')
        return CharacterAsset.objects.filter(character__id=character_id)
    