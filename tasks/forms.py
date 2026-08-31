from django import forms
from django.utils import timezone

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "priority", "deadline"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Task title",
                    "required": True,
                    "maxlength": Task._meta.get_field("title").max_length,
                }
            ),
            "priority": forms.Select(attrs={"required": True}),
            "deadline": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["deadline"].widget.attrs["min"] = timezone.localdate().isoformat()

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if not title:
            raise forms.ValidationError("Title cannot be empty.")
        return title

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if deadline and deadline < timezone.localdate():
            raise forms.ValidationError("Deadline cannot be in the past.")
        return deadline
