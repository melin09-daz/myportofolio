from django.forms import ModelForm, TextInput, Textarea, URLInput
from main.models import Experience, Project
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "start_month",
            "start_year",
            "end_month",
            "end_year",
            "is_ongoing",
            "logo",
        ]

        labels = {
            "title": "Judul Pengalaman",
            "description": "Deskripsi Pengalaman",
            "category": "Kategori Pengalaman",
            "start_month": "Bulan Mulai",
            "start_year": "Tahun Mulai",
            "end_month": "Bulan Akhir",
            "end_year": "Tahun Akhir",
            "is_ongoing": "Masih Berlangsung",
            "logo": "Logo",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Nama Pengalaman",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Pengalamanmu",
                    "rows": 3,
                }
            ),
            "category": TextInput(
                attrs={
                    "placeholder": "part-time",
                }
            ),
            "start_month": TextInput(
                attrs={
                    "placeholder": "1-12",
                }
            ),
            "start_year": TextInput(
                attrs={
                    "placeholder": "2025",
                }
            ),
            "end_month": TextInput(
                attrs={
                    "placeholder": "1-12",
                }
            ),
            "end_year": TextInput(
                attrs={
                    "placeholder": "2025",
                }
            ),
            "logo": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "category",
            "tech_stack",
            "repository_url",
            "demo_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "category": "Kategori Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "repository_url": "Repositori Proyek",
            "demo_url": "URL Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "category": TextInput(
                attrs={
                    "placeholder": "web-dev",
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "repository_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/melin09-daz/myportofolio",
                }
            ),
            "demo_url": URLInput(
                attrs={
                    "placeholder": "https://amelinda-fedora-myportofolio.pws.cs.ui.ac.id/",
                }
            ),
        }
        
        def clean_title(self):
            title = strip_tags(self.cleaned_data["title"]).strip()
            if not title:
                raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
            return title

        def clean_tech_stack(self):
            return strip_tags(self.cleaned_data["tech_stack"]).strip()

        def clean_description(self):
            return strip_tags(self.cleaned_data["description"]).strip()