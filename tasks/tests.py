from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.urls import reverse
from datetime import timedelta

from .models import Task
from .forms import TaskForm
from projects.models import Project


class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.project = Project.objects.create(owner=self.user, title='Test Project')
    
    def test_task_creation(self):
        task = Task.objects.create(project=self.project, title='Test Task', priority=Task.Priority.MEDIUM)
        self.assertEqual(task.title, 'Test Task')
        self.assertFalse(task.is_done)
    
    def test_task_clean_past_deadline_raises_error(self):
        past_date = timezone.localdate() - timedelta(days=1)
        task = Task(project=self.project, title='Task', deadline=past_date)
        with self.assertRaises(ValidationError):
            task.clean()
    
    def test_task_ordering_by_priority(self):
        Task.objects.create(project=self.project, title='Low', priority=Task.Priority.LOW)
        Task.objects.create(project=self.project, title='High', priority=Task.Priority.HIGH)
        tasks = list(Task.objects.filter(project=self.project))
        self.assertEqual(tasks[0].priority, Task.Priority.HIGH)
        self.assertEqual(tasks[1].priority, Task.Priority.LOW)


class TaskFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.project = Project.objects.create(owner=self.user, title='Test Project')
    
    def test_form_valid(self):
        data = {'title': 'Valid task', 'priority': Task.Priority.HIGH, 'deadline': ''}
        form = TaskForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_form_invalid_empty_title(self):
        data = {'title': '   ', 'priority': Task.Priority.MEDIUM, 'deadline': ''}
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())
    
    def test_form_invalid_past_deadline(self):
        past_date = timezone.localdate() - timedelta(days=1)
        data = {'title': 'Task', 'priority': Task.Priority.LOW, 'deadline': past_date}
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())


class TaskViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.project1 = Project.objects.create(owner=self.user1, title='Project1')
        self.project2 = Project.objects.create(owner=self.user2, title='Project2')
        self.task1 = Task.objects.create(project=self.project1, title='Task1')
        self.task2 = Task.objects.create(project=self.project2, title='Task2')
    
    def test_create_requires_login(self):
        response = self.client.get(reverse('tasks:create', kwargs={'project_id': self.project1.id}))
        self.assertEqual(response.status_code, 302)
    
    def test_create_own_project(self):
        self.client.login(username='user1', password='pass123')
        data = {'title': 'New task', 'priority': Task.Priority.HIGH, 'deadline': ''}
        response = self.client.post(reverse('tasks:create', kwargs={'project_id': self.project1.id}), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(project=self.project1, title='New task').exists())
    
    def test_update_own_task(self):
        self.client.login(username='user1', password='pass123')
        data = {'title': 'Updated', 'priority': Task.Priority.HIGH, 'deadline': ''}
        response = self.client.post(reverse('tasks:edit', kwargs={'pk': self.task1.id}), data=data)
        self.assertEqual(response.status_code, 200)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Updated')
    
    def test_delete_own_task(self):
        self.client.login(username='user1', password='pass123')
        task_id = self.task1.id
        self.client.post(reverse('tasks:delete', kwargs={'pk': self.task1.id}))
        self.assertFalse(Task.objects.filter(id=task_id).exists())
    
    def test_toggle_done_own_task(self):
        self.client.login(username='user1', password='pass123')
        self.assertFalse(self.task1.is_done)
        self.client.post(reverse('tasks:toggle', kwargs={'pk': self.task1.id}))
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.is_done)
    
    def test_cannot_access_other_user_task(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.post(reverse('tasks:delete', kwargs={'pk': self.task2.id}))
        self.assertEqual(response.status_code, 404)
