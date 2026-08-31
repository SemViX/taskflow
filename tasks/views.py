from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from projects.models import Project
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, View
from .models import Task
from .forms import TaskForm
from django.http import HttpResponse

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
        
        self.project = get_object_or_404(
            Project, pk=kwargs["project_id"], owner=request.user
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("task", None)
        context["project"] = self.project
        return context

    def form_valid(self, form):
        form.instance.project = self.project
        self.object = form.save()
        return render(self.request, "tasks/_task_row.html", {"task": self.object})

class TaskUpdateView(TaskQuerysetMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/_task_form.html"

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, "tasks/_task_row.html", {"task": self.object})

class TaskDetailPartialView(TaskQuerysetMixin, DetailView):
    def get(self, request, pk):
        task = get_object_or_404(self.get_queryset(), pk=pk)
        return render(request, "tasks/_task_row", {"task":task})

class TaskDeleteView(TaskQuerysetMixin, DeleteView):
    model = Task

    def post(self, request, *args, **kwargs):
        self.get_object().delete()
        return HttpResponse()
    
    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return HttpResponse()

class TaskToggleDoneView(TaskQuerysetMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(self.get_queryset(), pk=pk)
        task.is_done = not task.is_done
        task.save(update_fields=["is_done"])
        return render(request, "tasks/_task_row.html", {"task":task})