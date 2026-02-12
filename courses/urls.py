from django.urls import path
from . import views

from .views import (
    add_course,
    add_module,
    add_lesson,
    instructor_courses,
    course_detail, 
    lesson_detail# ⭐ MUST IMPORT
)

app_name = "courses"

urlpatterns = [

    # Instructor
    path("add-course/", add_course, name="add_course"),
    path("manage/", instructor_courses, name="instructor_courses"),
    path("add-module/<int:course_id>/", add_module, name="add_module"),
    path("add-lesson/<int:module_id>/", add_lesson, name="add_lesson"),
    

    # ⭐⭐ THIS FIXES YOUR ERROR
    path("course/<int:pk>/", course_detail, name="course_detail"),
    path("lesson/<int:pk>/", lesson_detail, name="lesson_detail"),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('my-courses/', views.student_courses, name='student_courses'),
    path('explore/', views.explore_courses, name='explore_courses'),


    


]
