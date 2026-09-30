from django.urls import path

from main.views import (show_main, show_experience, create_experience, edit_experience, get_experience_json, delete_experience, toggle_experience_star, show_project, 
                        create_project, edit_project, get_projects_json, delete_project, register, login_user, logout_user, toggle_star, create_project_ajax)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("experiences/add/", create_experience, name="create_experience"),
    path("experiences/<uuid:experience_id>/edit/", edit_experience, name="edit_experience"),
    path("api/experience/", get_experience_json, name="get_experience_json"),
    path("experiences/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("experiences/<uuid:experience_id>/star/", toggle_experience_star, name="toggle_experience_star"),
    path("project/", show_project, name="show_project"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/<uuid:project_id>/edit/", edit_project, name="edit_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/",delete_project,name="delete_project"),
    path("projects/<uuid:project_id>/star/", toggle_star, name="toggle_star",),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("projects/add-ajax/", create_project_ajax, name="create_project_ajax"),
]