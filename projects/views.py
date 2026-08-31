from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import ProjectForm
from .models import Project


# Create your views here.
class OwnerQuerysetMixin(LoginRequiredMixin):
    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class ProjectListView(OwnerQuerysetMixin, ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"


class MessagesPartialView(LoginRequiredMixin, TemplateView):
    template_name = "partials/_messages.html"


class ProjectCreateView(OwnerQuerysetMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/_project_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()
        messages.success(self.request, "Project created.")
        response = render(self.request, "projects/_project_card.html", {"project": self.object})
        response["HX-Trigger"] = "messagesChanged"
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the project form errors.")
        response = super().form_invalid(form)
        response["HX-Retarget"] = "#project-form-new"
        response["HX-Reswap"] = "outerHTML"
        response["HX-Trigger"] = "messagesChanged"
        return response


class ProjectUpdateView(OwnerQuerysetMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/_project_form.html"

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "Project updated.")
        response = render(self.request, "projects/_project_card.html", {"project": self.object})
        response["HX-Trigger"] = "messagesChanged"
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the project form errors.")
        response = super().form_invalid(form)
        response["HX-Trigger"] = "messagesChanged"
        return response


class ProjectDeleteView(OwnerQuerysetMixin, DeleteView):
    model = Project

    def post(self, request, *args, **kwargs):
        self.get_object().delete()
        messages.success(request, "Project deleted.")
        return HttpResponse(headers={"HX-Trigger": "messagesChanged"})

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        messages.success(request, "Project deleted.")
        return HttpResponse(headers={"HX-Trigger": "messagesChanged"})


class ProjectDetailView(OwnerQuerysetMixin, DetailView):
    model = Project
    template_name = "projects/_project_card.html"
    context_object_name = "project"
