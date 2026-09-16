from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import render
from django.db.utils import OperationalError, ProgrammingError
from main.models import Experience, Project
from main.forms import ProjectForm

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
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Amelinda Fedora Faragusti",
        "project_list": projects,
        "title_query": title_query,
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

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_project")

    return redirect("main:show_project")