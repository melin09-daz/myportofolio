from django.forms import ModelForm, TextInput, Textarea, URLInput

from main.models import Project

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