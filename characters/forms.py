from django import forms
from .models import Character, Vow, CharacterAsset, Bond
from rules.models import AssetDefinition

class CharBaseInfoForm(forms.Form):
    name = forms.CharField(max_length=100, label="Character Name")
    description = forms.CharField(widget=forms.Textarea, label="Character Description")

class CharStatsForm(forms.Form):
    edge = forms.IntegerField(min_value=1, max_value=3, label="Edge")
    heart = forms.IntegerField(min_value=1, max_value=3, label="Heart")
    iron = forms.IntegerField(min_value=1, max_value=3, label="Iron")
    shadow = forms.IntegerField(min_value=1, max_value=3, label="Shadow")
    wits = forms.IntegerField(min_value=1, max_value=3, label="Wits")
    
    def clean(self):
        cleaned_data = super().clean()
        stats:list = [
            cleaned_data.get('edge'),
            cleaned_data.get('heart'),
            cleaned_data.get('iron'),
            cleaned_data.get('shadow'),
            cleaned_data.get('wits'),
        ]
        
        # Check if all stats are present
        if None in stats:
            return cleaned_data
        
        # sort in descending order and compare to required distribution
        sorted_stats = sorted(stats, reverse=True)
        required_distribution = [3, 2, 2, 1, 1]
        if sorted_stats != required_distribution:
            raise forms.ValidationError(
                "Stats must be distributed as: one 3, two 2s, and two 1s (e.g., 3, 2, 2, 1, 1)."
            )
        
        return cleaned_data
    
class CharResoursesForm(forms.Form):
    experience = forms.IntegerField(label="Experience", initial=0, disabled=True )
    health = forms.IntegerField(label="Health", initial=5, disabled=True )
    spirit = forms.IntegerField(label="Spirit", initial=5, disabled=True )
    supply = forms.IntegerField(label="Supply", initial=5, disabled=True )
    momentum = forms.IntegerField(label="Momentum", initial=2, disabled=True )

    momentum_max = forms.IntegerField(initial=10, max_value=10, min_value=0, label="Max Momentum")
    momentum_reset = forms.IntegerField(initial=2, max_value=2, min_value=0, label="Momentum Reset")

class CharInitialBondsForm(forms.Form):
    bond_description_1 = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Bond 1 (Optional)",
        required=False
    )
    bond_description_2 = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Bond 2 (Optional)",
        required=False
    )
    bond_description_3 = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Bond 3 (Optional)",
        required=False
    )

class BackgroungVowForm(forms.Form):
    vow_title = forms.CharField()
    
    vow_description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label="Vow Description",
    )
    difficulty = forms.ChoiceField(
        choices=[(4, 'extreme'), (5, 'epic')],
        label="Vow Difficulty",
    )

class InitialAssetsForm(forms.Form):
    asset_definition_1 = forms.ChoiceField(
        label="Asset 1",
        required=False
    )
    asset_definition_2 = forms.ChoiceField(
        label="Asset 2",
        required=False
    )
    asset_definition_3 = forms.ChoiceField(
        label="Asset 3",
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate choices from AssetDefinition instances
        assets = AssetDefinition.objects.all()
        choices = [('', '--- Select an asset ---')] + [(asset.pk, asset.title) for asset in assets]
        
        self.fields['asset_definition_1'].choices = choices
        self.fields['asset_definition_2'].choices = choices
        self.fields['asset_definition_3'].choices = choices



class CharacterAssetForm(forms.ModelForm):
    class Meta:
        model = CharacterAsset
        fields = ["definition"]

class NewVowForm(forms.ModelForm):
    class Meta:
        model = Vow
        fields = ["title", "description", "difficulty"]

class NewBondForm(forms.ModelForm):
    class Meta:
        model = Bond
        fields = ["description"]