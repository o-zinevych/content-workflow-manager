from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from content.models import Position


class PositionForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        label="Name",
        widget=forms.TextInput(
            attrs={"placeholder": "Use Title Case"}
        )
    )

    class Meta:
        model = Position
        fields = "__all__"


class StaffCreationForm(UserCreationForm):
    position = forms.ModelMultipleChoiceField(
        queryset=Position.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "position",)
