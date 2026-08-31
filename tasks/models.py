from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from projects.models import Project


# Create your models here.
class Task(models.Model):
    class Priority(models.IntegerChoices):
        LOW = 1, "Low"
        MEDIUM = 2, "Medium"
        HIGH = 3, "High"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.MEDIUM)
    deadline = models.DateField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-priority", "order", "created_at"]

    def __str__(self):
        return self.title

    def clean(self):
        if self.deadline and self.deadline < timezone.localdate():
            raise ValidationError({"deadline": "Deadline cannot be in the past."})
