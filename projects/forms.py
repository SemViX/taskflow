from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "color"]
        widjets ={
            "title": forms.TextInput(attrs={"placeholder": "Назва проєкту"}),
            "color": forms.TextInput(attrs={"type": "color"})
        }

        def clean_title(self):
            title = self.cleaned_data["title"].strip()
            if not title:
                raise forms.ValidationError("Назва не може бути порожньою")
            return title