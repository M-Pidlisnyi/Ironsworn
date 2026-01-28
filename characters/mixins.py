from .models import Character
from django.shortcuts import get_object_or_404, redirect

class AddCharacterContextMixin:
    """
    Add a character instance to the view context.

    Expects a ``char_id`` keyword argument in the URL and provides the
    corresponding :model:`characters.Character` instance as ``character``
    in the template context.

    ``url_kwarg`` and ``context_name`` support overwriting.
    """
    url_kwarg = "char_id"
    context_name = "character"

    def get_character(self):
        """gets char_id from url and returns character with such id"""
        return get_object_or_404(
            Character,
            pk=self.kwargs[self.url_kwarg], #type: ignore
            user=self.request.user#type: ignore
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)#type: ignore
        context[self.context_name] = self.get_character()
        return context
    
class SaveCharacterAttributeMixin:
    """
        Attach a newly created object to a character and redirect to the
        character sheet.

        This mixin is intended for CreateView-based views that create objects
        related to a :model:`characters.Character`, such as vows or bonds.

        Expects a ``char_id`` keyword argument in the URL. Overwrite ``url_kwarg`` to change it.
        
        The name of the foreign key field can be customized by overriding
        ``field_name``. Assignment uses ``setattr`` to support this.
    """

    url_kwarg  = "char_id"
    field_name = "character"

    def form_valid(self, form):
        obj = form.save(commit=False)

        character_id = self.kwargs[self.url_kwarg]#type:ignore
        character = Character.objects.get(id=character_id)

        setattr(obj, self.field_name, character)
        obj.save()
        return redirect('characters:character-sheet', pk=character_id)
    
class BelongsToCharacterMixin:
    """
    Filter a queryset to objects belonging to a specific character.

    Restricts the queryset to objects related to the character identified by
    the ``char_id`` keyword argument in the URL. Useful for detail and delete
    views that operate on character-scoped objects.

    Expects a ``char_id`` keyword argument in the URL and ``url_kwarg``
    can be overridden to use a different parameter name.
    """
    url_kwarg = "char_id"

    def get_queryset(self):
        character_id = self.kwargs.get(self.url_kwarg)
        return self.model.objects.filter(character__id=character_id) 