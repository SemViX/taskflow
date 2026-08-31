import re

from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "color"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Project title",
                    "required": True,
                    "maxlength": Project._meta.get_field("title").max_length,
                }
            ),
            "color": forms.TextInput(attrs={"type": "color"}),
        }

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if not title:
            raise forms.ValidationError("Project title cannot be empty.")
        return title

    def clean_color(self):
        color = self.cleaned_data["color"]
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", color):
            raise forms.ValidationError("Enter a valid HEX color, for example #6c5ce7.")
        return color
