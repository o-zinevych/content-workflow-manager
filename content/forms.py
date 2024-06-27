from django import forms

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
