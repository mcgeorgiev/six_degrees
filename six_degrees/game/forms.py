from django import forms
from game.models import Game, UserProfile

class UserProfileForm(forms.ModelForm):
    picture = forms.ImageField(required=False)
    class Meta:
        model = UserProfile
        exclude = ('user',)
