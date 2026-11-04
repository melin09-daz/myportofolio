from django.test import TestCase, Client
from django.urls import reverse
from main.models import Experience, Project


class MainViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_main_url_is_exist(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_main_using_index_template(self):
        response = self.client.get('')
        self.assertTemplateUsed(response, 'index.html')


class ExperienceViewTest(TestCase):
    """Halaman Experience kini memuat data lewat AJAX dari API DRF,
    jadi HTML awalnya hanya berisi kerangka. Data diuji lewat endpoint API."""

    def setUp(self):
        self.client = Client()
        self.list_url = reverse('api:experience-list')

    def test_experience_url_is_exist_and_using_correct_template(self):
        response = self.client.get(reverse('main:show_experience'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'experience.html')

    def test_experience_page_has_ajax_skeleton(self):
        response = self.client.get(reverse('main:show_experience'))
        self.assertContains(response, 'id="grid"')
        self.assertContains(response, 'id="empty"')
        self.assertContains(response, 'Belum ada pengalaman yang ditambahkan atau ditemukan.')
        self.assertContains(response, self.list_url)

    def test_experience_empty_state(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_experience_with_data_ongoing(self):
        Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami dasar pengembangan web.",
            category="part-time",
            logo="/static/img/python1.png",
            start_year=2025,
            is_ongoing=True,
        )
        data = self.client.get(self.list_url).json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Asisten Dosen PBP")
        self.assertEqual(data[0]["description"], "Membantu mahasiswa memahami dasar pengembangan web.")
        self.assertIn("Sedang berlangsung", data[0]["period_display"])

    def test_experience_with_data_completed_shows_years(self):
        Experience.objects.create(
            title="UI/UX Design Intern",
            description="Mendesain user flow dan wireframe aplikasi mobile.",
            category="internship",
            logo="/static/img/figma1.png",
            start_year=2023,
            end_year=2024,
            is_ongoing=False,
        )
        data = self.client.get(self.list_url).json()
        self.assertEqual(data[0]["title"], "UI/UX Design Intern")
        self.assertEqual(data[0]["period_display"], "2023 - 2024")

    def test_experience_with_months_and_years(self):
        exp = Experience.objects.create(
            title="Product Management Intern",
            description="Mengelola backlog dan product roadmap.",
            category="internship",
            start_month=2,
            start_year=2024,
            end_month=8,
            end_year=2024,
            is_ongoing=False,
        )
        self.assertEqual(exp.period_display, "Februari 2024 - Agustus 2024")
        data = self.client.get(self.list_url).json()
        self.assertEqual(data[0]["period_display"], "Februari 2024 - Agustus 2024")


class ProjectViewTest(TestCase):
    """Sama seperti Experience: data Project diuji lewat API."""

    def setUp(self):
        self.list_url = reverse('api:project-list')

    def test_project_page_empty(self):
        response = self.client.get(reverse('main:show_project'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Projects")
        self.assertContains(response, 'id="grid"')
        self.assertContains(response, "Belum ada proyek yang ditambahkan atau ditemukan.")
        self.assertEqual(self.client.get(self.list_url).json(), [])

    def test_project_page_with_data(self):
        Project.objects.create(
            title="Portfolio Website Django",
            description="Personal website portfolio built with Django and responsive design.",
            category="web-dev",
            tech_stack="Python, Django, HTML, CSS",
            repository_url="https://github.com/melin09-daz/myportofolio",
            demo_url="https://example.com",
        )
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        item = response.json()[0]
        self.assertEqual(item["title"], "Portfolio Website Django")
        self.assertEqual(item["tech_stack"], "Python, Django, HTML, CSS")
        self.assertEqual(item["repository_url"], "https://github.com/melin09-daz/myportofolio")
        self.assertEqual(item["demo_url"], "https://example.com")