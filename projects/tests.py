from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Project


User = get_user_model()


class ProjectListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpass123")
        self.client.force_login(self.user)

    def test_requires_authentication(self):
        self.client.logout()
        response = self.client.get(reverse("projects:list"))
        self.assertEqual(response.status_code, 302)

    def test_returns_200(self):
        response = self.client.get(reverse("projects:list"))
        self.assertEqual(response.status_code, 200)

    def test_user_sees_only_own_projects(self):
        own_project = Project.objects.create(owner=self.user, title="My Project")
        other_user = User.objects.create_user(username="other", password="testpass123")
        Project.objects.create(owner=other_user, title="Other Project")
        
        response = self.client.get(reverse("projects:list"))
        self.assertContains(response, own_project.title)
        self.assertNotContains(response, "Other Project")


class ProjectCreateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpass123")
        self.client.force_login(self.user)

    def test_create_project_returns_200(self):
        response = self.client.get(reverse("projects:create"))
        self.assertEqual(response.status_code, 200)

    def test_create_project(self):
        response = self.client.post(reverse("projects:create"), {"title": "New Project", "color": "#ff0000"})
        self.assertEqual(response.status_code, 200)
        project = Project.objects.get(title="New Project")
        self.assertEqual(project.owner, self.user)

    def test_create_project_requires_authentication(self):
        self.client.logout()
        response = self.client.post(reverse("projects:create"), {"title": "New Project"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.count(), 0)


class ProjectUpdateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpass123")
        self.client.force_login(self.user)
        self.project = Project.objects.create(owner=self.user, title="Old Project", color="#000000",)

    def test_update_project(self):
        response = self.client.post(
            reverse(
                "projects:update",
                kwargs={"pk": self.project.pk},
            ),
            {
                "title": "Updated Project",
                "color": "#00ff00",
            },
            HTTP_HX_REQUEST="true",
        )
    
        self.assertEqual(response.status_code, 200)
    
        self.project.refresh_from_db()
    
        self.assertEqual(self.project.title, "Updated Project")
        self.assertEqual(self.project.color, "#00ff00")

    def test_cannot_update_other_users_project(self):
        other_user = User.objects.create_user(username="other", password="testpass123")
        other_project = Project.objects.create(owner=other_user, title="Other Project")
        
        response = self.client.post(
            reverse("projects:update", kwargs={"pk": other_project.pk}),
            {"title": "Hacked Project"}
        )
        self.assertEqual(response.status_code, 404)
        other_project.refresh_from_db()
        self.assertEqual(other_project.title, "Other Project")


class ProjectDeleteViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpass123")
        self.client.force_login(self.user)

    def test_delete_project(self):
        project = Project.objects.create(owner=self.user, title="Delete Me")
        response = self.client.post(reverse("projects:delete", kwargs={"pk": project.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Project.objects.filter(pk=project.pk).exists())

    def test_cannot_delete_other_users_project(self):
        other_user = User.objects.create_user(username="other", password="testpass123")
        project = Project.objects.create(owner=other_user, title="Other Project")
        
        response = self.client.post(reverse("projects:delete", kwargs={"pk": project.pk}))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Project.objects.filter(pk=project.pk).exists())


class ProjectDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpass123")
        self.client.force_login(self.user)
        self.project = Project.objects.create(owner=self.user, title="My Project")

    def test_detail_returns_200(self):
        response = self.client.get(reverse("projects:detail", kwargs={"pk": self.project.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My Project")

    def test_cannot_view_other_users_project(self):
        other_user = User.objects.create_user(username="other", password="testpass123")
        other_project = Project.objects.create(owner=other_user, title="Other Project")
        
        response = self.client.get(reverse("projects:detail", kwargs={"pk": other_project.pk}))
        self.assertEqual(response.status_code, 404)
