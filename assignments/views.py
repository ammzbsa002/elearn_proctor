from django.shortcuts import render

from django.contrib.auth.decorators import login_required

# Create your views here.

from django.shortcuts import render, redirect
from .forms import AssignmentForm
from courses.models import Course

@login_required
def add_assignment(request, course_id):

    course = Course.objects.get(id=course_id)

    if request.method == "POST":
        form = AssignmentForm(request.POST)

        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()

            return redirect("instructor_dashboard")

    else:
        form = AssignmentForm()

    return render(request, "instructor/add_assignment.html", {"form": form})




@login_required
def instructor_assignments(request):

    return render(request, "instructor/manage_assignments.html")

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from courses.models import Course


@login_required
def enroll_course(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    # Optional: prevent instructor enrolling in own course
    if hasattr(request.user, 'tutor'):
        return redirect('home')

    # Add student to course
    course.students.add(request.user)

    return redirect('student_courses')

@login_required
def student_courses(request):

    courses = Course.objects.filter(students=request.user)

    return render(request, "student/my_courses.html", {
        "courses": courses
    })



