from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import render
from django.db.utils import OperationalError, ProgrammingError
from main.models import Experience, Project, ProjectForm

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
        "experience_list": experience_list,
    }
    return render(request, "experience.html", context)

def show_project(request):
    try:
        project_list = list(Project.objects.all())
    except (OperationalError, ProgrammingError):
        from django.core.management import call_command
        try:
            call_command('migrate', interactive=False)
            project_list = list(Project.objects.all())
        except Exception:
            project_list = []
            
    context = {
        "name": "Amelinda Fedora Faragusti",
        "project_list": project_list,
    }
    return render(request, "project.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Amelinda Fedora Faragusti",
        "form": form,
    }
    return render(request, "projects_form.html", context)
