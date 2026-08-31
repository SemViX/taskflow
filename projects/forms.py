from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "color"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Project title"}),
            "color": forms.TextInput(attrs={"type": "color"}),
        }

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if not title:
            raise forms.ValidationError("Project title cannot be empty.")
        return title
