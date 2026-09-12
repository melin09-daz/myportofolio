from django.shortcuts import render
from django.db.utils import OperationalError, ProgrammingError
from main.models import Experience


def show_main(request):
    context = {
        "name": "Amelinda Fedora Faragusti",
        "npm": "2506540475",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Computer Science student at Universitas Indonesia. Currently focused on exploring data science and artificial intelligence, with a growing interest in how these fields can solve real-world problems. Always looking for new projects to learn from."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    try:
        experience_list = list(Experience.objects.all())
    except (OperationalError, ProgrammingError):
        from django.core.management import call_command
        try:
            call_command('migrate', interactive=False)
            experience_list = list(Experience.objects.all())
        except Exception:
            experience_list = []
            
    context = {
        "name": "Amelinda Fedora Faragusti",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)