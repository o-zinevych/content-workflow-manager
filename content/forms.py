from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    ReadOnlyPasswordHashField
)
from django.core.exceptions import ValidationError

from content.models import Position, Task, ContentType


class ContentTypeForm(forms.ModelForm):
    class Meta:
        model = ContentType
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data["name"]
        if not name.islower():
            raise ValidationError(
                f"Content type names should be lowercase, "
                f"for example, \"{name.lower()}\"."
            )
        return name


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data["name"]
        if not name.istitle():
            raise ValidationError(
                f"Position names should be in title case, for example, "
                f"\"{name.title()}\"."
            )
        return name


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search positions"})
    )


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


class StaffChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text="Raw passwords are not stored, so there is no way to see "
                  "this user's password."
    )
    position = forms.ModelMultipleChoiceField(
        queryset=Position.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "email",
            "position",
        )


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
