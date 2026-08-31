from django.conf import settings
from django.db import models
from django.urls import reverse


# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects"
    )
    title = models.CharField(max_length=100)
    color = models.CharField(
        max_length=7,
        default="#6c5ce7",
        help_text="HEX-колір шапки проєкту, напр. #6c5ce7",
    )
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projects:list")
