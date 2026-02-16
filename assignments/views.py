from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Assignment, Question
from .forms import AssignmentForm
from courses.models import Course


# ==========================================
# REDIRECT FROM DASHBOARD
# ==========================================
@login_required
def instructor_assignments_redirect(request):

    course = Course.objects.filter(tutor=request.user.tutor).first()

    if course:
        return redirect(
            "assignments:instructor_assignments",
            course_id=course.id
        )

    return redirect("instructor_dashboard")


# ==========================================
# MANAGE ASSIGNMENTS (PER COURSE)
# ==========================================
@login_required
def instructor_assignments(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    assignments = Assignment.objects.filter(course=course)

    return render(request, "instructor/manage_assignments.html", {
        "course": course,
        "assignments": assignments
    })


# ==========================================
# ADD ASSIGNMENT + MCQs
# ==========================================
@login_required
def add_assignment(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        form = AssignmentForm(request.POST)

        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()

            questions = request.POST.getlist("question_text")
            options_a = request.POST.getlist("option_a")
            options_b = request.POST.getlist("option_b")
            options_c = request.POST.getlist("option_c")
            options_d = request.POST.getlist("option_d")
            correct_answers = request.POST.getlist("correct_answer")

            for i in range(len(questions)):
                if questions[i].strip() != "":
                    Question.objects.create(
                        assignment=assignment,
                        question_text=questions[i],
                        option_a=options_a[i],
                        option_b=options_b[i],
                        option_c=options_c[i],
                        option_d=options_d[i],
                        correct_answer=correct_answers[i],
                    )

            return redirect(
                "assignments:instructor_assignments",
                course_id=course.id
            )

    else:
        form = AssignmentForm()

    return render(request, "instructor/add_assignment.html", {
        "assignment_form": form,
        "course": course
    })
