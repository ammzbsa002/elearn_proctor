from django.urls import path
from . import views

app_name = "assignments"

urlpatterns = [

    # Redirect from dashboard
    path(
        "manage/",
        views.instructor_assignments_redirect,
        name="instructor_assignments_redirect"
    ),

    # Manage assignments per course
    path(
        "manage/<int:course_id>/",
        views.instructor_assignments,
        name="instructor_assignments"
    ),

    # Add assignment per course
    path(
        "add/<int:course_id>/",
        views.add_assignment,
        name="add_assignment"
    ),
]
