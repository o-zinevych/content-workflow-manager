from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from content.models import Position, Task


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


class TaskForm(forms.ModelForm):
    deadline = forms.DateField(
        label="Deadline",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )
    staff = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Task
        fields = "__all__"
