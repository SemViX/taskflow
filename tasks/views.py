from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, View

from projects.models import Project

from .forms import TaskForm
from .models import Task


# Create your views here
class TaskQuerysetMixin(LoginRequiredMixin):
    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/_task_form.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        self.project = get_object_or_404(Project, pk=kwargs["project_id"], owner=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("task", None)
        context["project"] = self.project
        return context

    def form_valid(self, form):
        form.instance.project = self.project
        self.object = form.save()
        messages.success(self.request, "Task created.")
        response = render(self.request, "tasks/_task_row.html", {"task": self.object})
        response["HX-Trigger"] = "messagesChanged"
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the task form errors.")
        response = super().form_invalid(form)
        response["HX-Retarget"] = "#task-new"
        response["HX-Reswap"] = "outerHTML"
        response["HX-Trigger"] = "messagesChanged"
        return response


class TaskUpdateView(TaskQuerysetMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/_task_form.html"

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "Task updated.")
        response = render(self.request, "tasks/_task_row.html", {"task": self.object})
        response["HX-Trigger"] = "messagesChanged"
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the task form errors.")
        response = super().form_invalid(form)
        response["HX-Trigger"] = "messagesChanged"
        return response


class TaskDetailPartialView(TaskQuerysetMixin, DetailView):
    def get(self, request, pk):
        task = get_object_or_404(self.get_queryset(), pk=pk)
        return render(request, "tasks/_task_row.html", {"task": task})


class TaskDeleteView(TaskQuerysetMixin, DeleteView):
    model = Task

    def post(self, request, *args, **kwargs):
        self.get_object().delete()
        messages.success(request, "Task deleted.")
        return HttpResponse(headers={"HX-Trigger": "messagesChanged"})

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        messages.success(request, "Task deleted.")
        return HttpResponse(headers={"HX-Trigger": "messagesChanged"})


class TaskToggleDoneView(TaskQuerysetMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(self.get_queryset(), pk=pk)
        task.is_done = not task.is_done
        task.save(update_fields=["is_done"])
        messages.success(
            request, "Task marked as done." if task.is_done else "Task marked as active."
        )
        response = render(request, "tasks/_task_row.html", {"task": task})
        response["HX-Trigger"] = "messagesChanged"
        return response
