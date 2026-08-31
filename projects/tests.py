from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class ProjectListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpass123")
        self.client.force_login(self.user)

    def test_add_project_button_stays_visible_when_form_is_opened(self):
        response = self.client.get(reverse("projects:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "+ Add Project List")
        self.assertContains(response, 'id="project-form-container"')
        self.assertContains(response, 'hx-target="#project-form-container"')
        self.assertNotContains(response, 'hx-target="this"')
