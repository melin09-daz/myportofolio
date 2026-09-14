from django.test import TestCase, Client
from django.urls import reverse
from main.models import Experience


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
    def setUp(self):
        self.client = Client()

    def test_experience_url_is_exist_and_using_correct_template(self):
        response = self.client.get(reverse('main:show_experience'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'experience.html')

    def test_experience_empty_state(self):
        response = self.client.get(reverse('main:show_experience'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Belum ada pengalaman yang ditambahkan.')

    def test_experience_with_data_ongoing(self):
        exp = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami dasar pengembangan web.",
            category="part-time",
            logo="/static/img/python1.png",
            start_year=2025,
            is_ongoing=True,
        )
        response = self.client.get(reverse('main:show_experience'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Asisten Dosen PBP")
        self.assertContains(response, "Membantu mahasiswa memahami dasar pengembangan web.")
        self.assertContains(response, "Sedang berlangsung")

    def test_experience_with_data_completed_shows_years(self):
        exp = Experience.objects.create(
            title="UI/UX Design Intern",
            description="Mendesain user flow dan wireframe aplikasi mobile.",
            category="internship",
            logo="/static/img/figma1.png",
            start_year=2023,
            end_year=2024,
            is_ongoing=False,
        )
        response = self.client.get(reverse('main:show_experience'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "UI/UX Design Intern")
        self.assertContains(response, "2023 - 2024")

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
        response = self.client.get(reverse('main:show_experience'))
        self.assertContains(response, "Februari 2024 - Agustus 2024")
        
class ProjectViewTest(TestCase):
    def test_project_page_empty(self):
        response = self.client.get(reverse('main:show_project'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Projects")
        self.assertContains(response, "Belum ada project yang ditambahkan.")

    def test_project_page_with_data(self):
        from main.models import Project
        proj = Project.objects.create(
            title="Portfolio Website Django",
            description="Personal website portfolio built with Django and responsive design.",
            category="web-dev",
            tech_stack="Python, Django, HTML, CSS",
            repository_url="https://github.com/melin09-daz/myportofolio",
            demo_url="https://example.com"
        )
        response = self.client.get(reverse('main:show_project'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Portfolio Website Django")
        self.assertContains(response, "Python, Django, HTML, CSS")
        self.assertContains(response, "Repository")
        self.assertContains(response, "Live Demo")