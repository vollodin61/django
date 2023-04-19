from django import forms
from django.forms import ImageField, ClearableFileInput

from myauth.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"

    images = ImageField(
            widget=ClearableFileInput(attrs={'multiple': True}),
        )
