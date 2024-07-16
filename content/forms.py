from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from content.models import Task, ContentType


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


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by task or staff"}
        )
    )
