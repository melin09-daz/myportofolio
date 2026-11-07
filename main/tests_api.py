import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Experience, Project


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.project = Project.objects.create(
            title="Portfolio", description="My website", tech_stack="Django",
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project", "description": "A useful app",
            "category": "web-dev", "tech_stack": "Python",
            "repository_url": "https://github.com/example/repo",
            "demo_url": "https://example.com/",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": " "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"demo_url": "javascript:alert(1)"}, "demo_url"),
            ({"repository_url": "javascript:alert(1)"}, "repository_url"),
            ({"category": "bukan-kategori"}, "category"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, changes)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "My website")
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_editor_can_update_but_not_create_or_delete_projects(self):
        editor = User.objects.create_user(username="editor-user", password="test-password")
        editor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=editor)
        response = self.client.patch(self.detail_url, {"title": "Diubah Editor"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Diubah Editor")
        self.assertEqual(self.project.description, "My website")
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 200)
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertTrue(Project.objects.filter(pk=self.project.id).exists())
        self.assertEqual(Project.objects.count(), 1)

    def test_staff_without_editor_group_cannot_manage_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        # The Browsable API form renders a real CSRF token into the response.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_owner_patch_can_clear_optional_urls(self):
        self.project.demo_url = "https://example.com/"
        self.project.save()
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(
            self.detail_url,
            {"title": "Judul Baru", "category": "web-dev", "demo_url": None},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Judul Baru")
        self.assertIsNone(self.project.demo_url)

    def test_edit_modal_only_rendered_for_owner_and_editor(self):
        editor = User.objects.create_user(username="editor-user", password="test-password")
        editor.groups.add(Group.objects.create(name="Editor"))
        page = reverse("main:show_project")
        for user, expected in [(self.visitor, False), (editor, True), (self.owner, True)]:
            self.client.force_login(user)
            html = self.client.get(page).content.decode()
            self.assertEqual('id="project-edit-form"' in html, expected, user.username)


class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.editor = User.objects.create_user(username="editor", password="test-password")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.experience = Experience.objects.create(
            title="Asisten Dosen", description="Membantu mahasiswa", category="part-time",
            start_month=2, start_year=2024, end_month=8, end_year=2024, is_ongoing=False,
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", args=[self.experience.id])
        self.star_url = reverse("api:experience-star", args=[self.experience.id])
        self.payload = {
            "title": "Research Intern", "description": "Riset AI", "category": "research",
            "start_month": 1, "start_year": 2025, "is_ongoing": True,
            "logo": "https://example.com/logo.png",
        }

    def test_public_list_and_period(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["period_display"], "Februari 2024 - Agustus 2024")
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(self.list_url, {"title": "zzz"}).data, [])

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "X"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)

    def test_editor_can_update_but_not_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"title": "Diubah"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertTrue(Experience.objects.filter(pk=self.experience.id).exists())

    def test_owner_crud(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["is_ongoing"])
        response = self.client.patch(self.detail_url, {"title": "Diubah"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_204_NO_CONTENT)

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": " "}, "title"),
            ({"title": "<b></b>"}, "title"),
            ({"category": "bukan-kategori"}, "category"),
            ({"start_month": 13}, "start_month"),
            ({"logo": "javascript:alert(1)"}, "logo"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, changes)
            self.assertIn(field, response.data)
        self.assertEqual(Experience.objects.count(), 1)

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_denied_writes_do_not_change_database(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.client.patch(self.detail_url, {"title": "Diretas"}, format="json")
            self.client.delete(self.detail_url)
            self.client.post(self.list_url, self.payload, format="json")
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Asisten Dosen")
        self.assertEqual(Experience.objects.count(), 1)

    def test_editor_patch_and_put_change_database(self):
        self.client.force_authenticate(user=self.editor)
        self.client.patch(self.detail_url, {"title": "Diubah Editor"}, format="json")
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Diubah Editor")
        self.assertEqual(self.experience.description, "Membantu mahasiswa")
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Research Intern")

    def test_staff_without_editor_group_cannot_update(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Diretas"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_missing_experience(self):
        url = reverse("api:experience-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        client.get(self.list_url, HTTP_ACCEPT="text/html")
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ExperienceLegacyViewConsistencyTest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser("owner", "o@example.com", "test-password")
        self.visitor = User.objects.create_user("visitor", password="test-password")
        self.staff = User.objects.create_user("staff", password="test-password", is_staff=True)
        self.lookalike = User.objects.create_user("editor", password="test-password")
        self.editor = User.objects.create_user("realeditor", password="test-password")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.experience = Experience.objects.create(
            title="Asisten Dosen", description="Membantu", category="part-time",
        )
        self.edit_url = reverse("main:edit_experience", args=[self.experience.id])
        self.page_url = reverse("main:show_experience")

    def test_only_owner_and_editor_group_open_legacy_edit_page(self):
        for user, expected in [
            (self.visitor, 403), (self.staff, 403), (self.lookalike, 403),
            (self.editor, 200), (self.owner, 200),
        ]:
            self.client.force_login(user)
            self.assertEqual(self.client.get(self.edit_url).status_code, expected, user.username)

    def test_legacy_delete_is_owner_only(self):
        self.client.force_login(self.editor)
        url = reverse("main:delete_experience", args=[self.experience.id])
        self.assertEqual(self.client.post(url).status_code, 403)
        self.assertTrue(Experience.objects.filter(pk=self.experience.id).exists())

    def test_edit_modal_only_rendered_for_owner_and_editor(self):
        for user, expected in [(self.visitor, False), (self.staff, False),
                               (self.editor, True), (self.owner, True)]:
            self.client.force_login(user)
            response = self.client.get(self.page_url)
            self.assertEqual('id="experience-edit-form"' in response.content.decode(), expected, user.username)