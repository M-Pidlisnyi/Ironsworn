from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.http import HttpRequest

from .forms import NewWorldForm, WorldTruthsForm
from .models import World, WorldTruth

# Create your views here.
class NewWorldView(CreateView):
    model = World
    form_class = NewWorldForm
    template_name = "generic_form.html"
    
    def form_valid(self, form) :
        new_world: World = form.save(commit=False)
        new_world.user = self.request.user #type: ignore
        new_world.save()
        return redirect("worlds:set-truths", pk=new_world.pk)
    

def set_wordlTruths(request: HttpRequest, pk: int):
    form = WorldTruthsForm(request.POST or None)
    world=World.objects.get(id=pk)
    if request.method == "POST":
        if form.is_valid():
            for question, _ in WorldTruth.QUESTIONS:
                WorldTruth.objects.create(
                    world=world,
                    question = question,
                    answer = form.cleaned_data.get(f"{question}_answer"),
                    quest_starter = form.cleaned_data.get(f"{question}_quest_starter")
                )
            
            return redirect("worlds:world-detail", pk=pk)

    return render(request, "worlds/worldtruths_form.html", {"world": world, "form": form})