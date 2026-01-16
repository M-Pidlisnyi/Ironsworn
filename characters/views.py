from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

from domain import progress_track as pt

from rules.models import AssetDefinition

from .models import Character, Bond, Vow, CharacterAsset, Debility, MinorQuest, CharacterAssetComponent, CharacterAssetAbility
from .forms import *
from .mixins import AddCharacterContextMixin, SaveCharacterAttributeMixin, BelongsToCharacterMixin

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
    """
    Guide the user through multi-stage character creation.

    This view implements a staged character creation workflow, where each
    stage collects a portion of the character’s starting data according to
    Ironsworn rules. Form data from each stage is accumulated in the user
    session until the final stage is completed.

    The current stage is controlled by the ``stage`` query parameter. If
    the parameter is missing or invalid, the first stage is shown.

    On successful completion of the final stage, the collected session
    data is used to create a new :model:`characters.Character`.

    This view requires authentication.

    **Template:**
    Renders the :template:`characters/character_creation.html` template. 
    The template consecutevly displays each from defined in ``CC_STAGES_FORMS`` constant

    **Context**

    ``form``
        The form instance corresponding to the current character creation
        stage.

    **Session State**

    ``char_creation_data``
        A dictionary stored in the session containing accumulated character
        creation data from previous stages.
        Each entry in the dictionary corresponds either to a field on
        :model:`characters.Character` or to data used to initialize related
        objects such as CharacterAssets, vows, or bonds.

    **Flow**

    - GET requests render the form for the current stage.
    - POST requests validate and store stage data in the session.
    - Intermediate stages redirect to the next stage.
    - The final stage creates the character and exits the workflow.
    """

    #stage number validation
    try:
        stage = int(request.GET.get('stage', 1))
    except ValueError:
        stage = 1
    if stage < 1 or stage > len(CC_STAGES_FORMS):
        stage = 1 

    #get form corresponding to current stage
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
    vow_title: str = data.pop('vow_title', '')
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
            title=vow_title,
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
    return redirect('characters:character-sheet', pk=character.pk)

class CharacterSheetView(DetailView):
    """
    Display the complete character sheet for an Ironsworn character.

    This view presents the full mechanical state of a single
    :model:`characters.Character`, formatted to match the official
    Ironsworn character sheet. It is the primary in-play view used during
    gameplay.

    In addition to the character instance, the view prepares tracker data
    and categorized debility lists required for rendering progress tracks,
    resource boxes, and condition checklists.

    As an intented side effect, the viewed character is stored in the user session
    as the most recently accessed character.

    **Template:**
    Renders the :template:`characters/character_sheet.html` template.

    **Context**

    ``character`` / ``object``
        The :model:`characters.Character` being displayed.

    ``momentum_tracker``
        A list or sequence of ``int`` defining the momentum track range, sourced
        from ``MOMENTUM_TRACK`` constant in project settings.

    ``difficulty_tracker``
        A list of difficulty rank labels used to render vow and bond
        progress tracks, sourced from ``DIFFICULTY_LEVELS`` constant in project settings.

    ``statuses``
        A list of resource name and value pairs representing the
        character’s current health, spirit, and supply.

    ``status_tracker``
        A list or sequence of ``int`` defining the resource track range, sourced
        from ``RESOURCE_TRACK`` constant in project settings.

    ``conditions_list``
        A list of all possible condition debility identifiers, sourced from ``characters.models.Debility.DEBILITIES`` constant.

    ``char_conditions``
        A list of condition debilities currently affecting the character.

    ``banes_list``
        A list of all possible bane debility identifiers, sourced from ``characters.models.Debility.DEBILITIES`` constant.

    ``char_banes``
        A list of bane debilities currently affecting the character.

    ``burdens_list``
        A list of all possible burden debility identifiers, sourced from ``characters.models.Debility.DEBILITIES`` constant.

    ``char_burdens``
        A list of burden debilities currently affecting the character.
    """

    model = Character
    template_name = 'characters/character_sheet.html'

    def get_context_data(self, **kwargs):
        context  = super().get_context_data(**kwargs)
        
        character:Character = self.get_object() # type: ignore
        
        # Save last viewed character to session
        self.request.session['last_character_id'] = character.pk
        self.request.session.modified = True
        
        context["momentum_tracker"] = settings.MOMENTUM_TRACK
        context["difficulty_tracker"] = [dif[1] for dif in settings.DIFFICULTY_LEVELS]
    
        context["statuses"] = [
            ("HEALTH", character.health),
            ("SPIRIT", character.spirit),
            ("SUPPLY", character.supply)
        ]
        context["status_tracker"] = settings.RESOURCE_TRACK

        debilities = Debility.DEBILITIES#format: [("deb_name", "verbose_deb_type: verbose_deb_name"), ...]
        context["conditions_list"] = [d[0] for d in debilities if "Condition" in d[1]]
        context["char_conditions"] = [d.name for d in self.get_object().debilities.filter(type="cond")] # type: ignore

        context["banes_list"] = [d[0] for d in debilities if "Bane" in d[1]]
        context["char_banes"] = [d.name for d in self.get_object().debilities.filter(type="bane")]# type: ignore

        context["burdens_list"] = [d[0] for d in debilities if "Burden" in d[1]]
        context["char_burdens"] = [d.name for d in self.get_object().debilities.filter(type="burd")]# type: ignore

        return context

class CharacterListView(ListView):
    """
    Display the list of characters owned by the current user.

    This view lists all :model:`characters.Character` instances associated
    with the authenticated user. 

    **Template:**
    Renders the :template:`characters/character_list.html` template.

    **Context**

    ``character_list``
        A queryset of :model:`characters.Character` objects owned by the current user.
    """
    model = Character

    def get_queryset(self):
        return Character.objects.filter(user=self.request.user)
    
class AddAssetView(AddCharacterContextMixin, SaveCharacterAttributeMixin, CreateView):
    """
    Add a new asset to a character.

    This view allows a player to select an :model:`rules.AssetDefinition` object and attach it
    to a specific :model:`characters.Character`, creating a new
    :model:`characters.CharacterAsset` instance.

    The character is identified by the ``char_id`` URL parameter.

    **Template:**
    Renders the :template:`characters/add_asset.html` template.

    **Context**

    ``form``
        A form used to select an asset definition to add to the character.
        
        fields: ``definition``, an HTML ``<select>`` element, with each ``<option>`` being an :model:`rules.AssetDefinition` object

    ``character``
        The :model:`characters.Character` to which the asset will be added.
    """

    model = CharacterAsset
    template_name = 'generic_form.html'
    form_class = CharacterAssetForm

class CharacterAssetsListView(AddCharacterContextMixin, ListView):
    """
    Display the list of assets owned by a character.

    This view lists all :model:`characters.CharacterAsset` instances
    associated with a specific :model:`characters.Character`. It is used
    to review, manage, or reference a character’s assets during play.

    The character is identified by the ``char_id`` URL parameter.

    **Template:**
    Renders the :template:`characters/characterasset_list.html` template.

    **Context**

    ``assets_list``
        A queryset of :model:`characters.CharacterAsset` objects owned by the character.

    ``character``
        The :model:`characters.Character` whose assets are being displayed.
    """
     
    model = CharacterAsset
    context_object_name = 'assets_list'

    def get_queryset(self):
        character_id = self.kwargs.get('char_id')
        return CharacterAsset.objects.filter(character__id=character_id)    

class CharacterBondsList(BelongsToCharacterMixin, AddCharacterContextMixin, ListView):
    model = Bond
    
class NewBondView(AddCharacterContextMixin, SaveCharacterAttributeMixin, CreateView):
    model = Bond
    form_class = NewBondForm
    template_name = 'generic_form.html'

class NewVowView(AddCharacterContextMixin, SaveCharacterAttributeMixin, CreateView):
    model = Vow
    form_class = NewVowForm
    template_name = 'generic_form.html'

class MinorQuestsListView(BelongsToCharacterMixin, AddCharacterContextMixin, ListView):
    model = MinorQuest
    context_object_name = "quests_list"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["difficulty_tracker"] = [dif[1] for dif in settings.DIFFICULTY_LEVELS]
        return context
    
class CharacterAssetEditView(AddCharacterContextMixin, DetailView):
    model = CharacterAsset
    template_name = "characters/characterasset_edit.html"
    context_object_name = "asset"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CharacterAssetEditForm(self.get_object())
        return context
    
    def post(self, request: HttpRequest, *args, **kwargs):
        asset:CharacterAsset = self.get_object()
        
        print(request.POST)
        for key, value in request.POST.items():
            if key.startswith("component_"):
                edited_component:CharacterAssetComponent = asset.components.get(definition__title=key.replace("component_", ""))
                edited_component.value = value
                edited_component.save()
            elif key.startswith("ability_"):
                #only inactive abilities can be turned on, you can't turn off already activated ability
                edited_ability:CharacterAssetAbility = asset.abilities.get(definition__title=key.replace("ability_", ""))
                edited_ability.is_active = True
                edited_ability.save()

        return redirect("characters:character-assets-list", char_id=self.get_object().character.id)
    
class NewMinorQuestView(AddCharacterContextMixin, SaveCharacterAttributeMixin, CreateView):
    model = MinorQuest
    form_class = NewMinorQuestForm
    template_name = "generic_form.html"

class CharacterVowsListView(BelongsToCharacterMixin, AddCharacterContextMixin, ListView):
    model = Vow

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["difficulty_tracker"] = [dif[1] for dif in settings.DIFFICULTY_LEVELS]
        return context


