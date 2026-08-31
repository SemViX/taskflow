from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project
from .forms import ProjectForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import HttpResponse

# Create your views here.
class OwnerQuerysetMixin(LoginRequiredMixin):
    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class ProjectListView(OwnerQuerysetMixin, ListView):
    model=Project
    template_name="projects/project_list.html"
    context_object_name = 'projects'

class ProjectCreateView(OwnerQuerysetMixin, CreateView):
    model = Project
    form_class=ProjectForm
    template_name="projects/_project_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()
        return render(
            self.request, "projects/_project_card.html", {"project":self.object}
        )

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response["HX-Retarget"] = "#project-form-new"
        response["HX-Reswap"] = "outerHTML"
        return response

class ProjectUpdateView(OwnerQuerysetMixin, UpdateView):
    model = Project
    form_class=ProjectForm
    template_name="projects/_project_form.html"

    def form_valid(self, form):
        self.object = form.save()
        return render(
            self.request, "projects/_project_card.html", {"project": self.object}
        )

class ProjectDeleteView(OwnerQuerysetMixin, DeleteView):
    model = Project

    def post(self, request, *args, **kwargs):
        self.get_object().delete()
        return HttpResponse()

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return HttpResponse()

class ProjectDetailView(OwnerQuerysetMixin, DetailView):
    model = Project
    template_name="projects/_project_card.html"
    context_object_name="project"
