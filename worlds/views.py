from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView
from django.http import HttpRequest

from .forms import NewWorldForm, WorldTruthsForm
from .models import World, WorldTruth


class WorldsListView(LoginRequiredMixin, ListView):
    """
    Display all worlds owned by the current user.

    This view lists all :model:`worlds.World` instances associated with
    the authenticated user.

    **Template:**
    Renders the default list template for :model:`worlds.World`.
    """
    model = World

    def get_queryset(self):
        return World.objects.filter(user=self.request.user)

class NewWorldView(LoginRequiredMixin, CreateView):
    """
    Create a new world.

    This view allows a user to create a new :model:`worlds.World`.
    After successful creation, redirects to the world truths form where
    the user answers worldbuilding questions.

    **Template:**
    Renders the :template:`generic_form.html` template.
    """
    model = World
    form_class = NewWorldForm
    template_name = "generic_form.html"
    
    def form_valid(self, form) :
        new_world: World = form.save(commit=False)
        new_world.user = self.request.user #type: ignore
        new_world.save()
        return redirect("worlds:set-truths", pk=new_world.pk)
    

@login_required
def set_wordlTruths(request: HttpRequest, pk: int):
    """
    Set worldbuilding truths for a newly created world.

    This view presents a form for the user to answer predefined worldbuilding
    questions and optionally provide quest starters for each.

    On POST with valid form data, creates :model:`worlds.WorldTruth` instances
    for all questions with the user's answers, then redirects to the world detail view.

    The world is identified by the ``pk`` URL parameter.

    **Template:**
    Renders the :template:`worlds/worldtruths_form.html` template.
    """
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