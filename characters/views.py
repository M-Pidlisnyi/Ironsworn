from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, ListView
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Character, Bond
from .forms import CharBaseInfoForm, CharStatsForm, CharResoursesForm, CharBondsForm

CC_STAGES_FROMS = [
    CharBaseInfoForm,
    CharStatsForm,
    CharResoursesForm,
    CharBondsForm
]

@login_required
def character_creation(request: HttpRequest):
    try:
        stage = int(request.GET.get('stage', 1))
    except ValueError:
        stage = 1
    if stage < 1 or stage > len(CC_STAGES_FROMS):
        stage = 1 

    form_class = CC_STAGES_FROMS[stage - 1]

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            # Save form data to session
            if 'char_creation_data' not in request.session:
                request.session['char_creation_data'] = {}
            request.session['char_creation_data'].update(form.cleaned_data)
            request.session.modified = True
           
            if stage < len(CC_STAGES_FROMS):
                return redirect(request.path + f'?stage={stage+1}')
            else:
                return save_character(request)
    else:
        form = form_class()

    return render(request, 'characters/character_creation.html', {'form': form})

def save_character(request: HttpRequest) -> HttpResponse:
    data = request.session.get('char_creation_data', {})
    
    # Extract bond descriptions from data (they shouldn't be saved to Character model)
    bond_descriptions = [
        data.pop('bond_description_1', ''),
        data.pop('bond_description_2', ''),
        data.pop('bond_description_3', ''),
    ]
  
    character = Character.objects.create(user=request.user, **data)
    
    # Create Bond objects for non-empty descriptions
    bond_count = 0
    for description in bond_descriptions:
        if description.strip():
            Bond.objects.create(character=character, description=description)
            bond_count += 1
    character.bonds_progress = bond_count
    character.save()

    del request.session['char_creation_data']
    return redirect('character-sheet', pk=character.pk)

class CharacterSheetView(DetailView):
    model = Character
    template_name = 'characters/character_sheet.html'

class CharacterListView(ListView):
    model = Character

    def get_queryset(self):
        return Character.objects.filter(user=self.request.user)