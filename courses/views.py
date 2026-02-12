from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from courses.models import Course, Tutor, Module, Lesson, LessonProgress
from .forms import CourseForm, ModuleForm, LessonForm


# =====================================
# HOME
# =====================================
def home(request):
    courses = Course.objects.order_by('-id')[:6]
    return render(request, 'home.html', {'courses': courses})


# =====================================
# INSTRUCTOR COURSES
# =====================================
@login_required
def instructor_courses(request):

    tutor = get_object_or_404(Tutor, user=request.user)

    courses = Course.objects.filter(
        tutor=tutor
    ).prefetch_related('modules')

    return render(request, "instructor/manage_courses.html", {
        "courses": courses
    })


# =====================================
# ADD COURSE
# =====================================
@login_required
def add_course(request):

    tutor = get_object_or_404(Tutor, user=request.user)

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)

        if form.is_valid():
            course = form.save(commit=False)
            course.tutor = tutor
            course.save()

            form.save_m2m()

            return redirect("instructor_dashboard")

    else:
        form = CourseForm()

    return render(request, "instructor/add_course.html", {
        "form": form
    })


# =====================================
# ADD MODULE
# =====================================
@login_required
def add_module(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    if request.user != course.tutor.user:
        return redirect("home")

    if request.method == "POST":
        form = ModuleForm(request.POST)

        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()

            return redirect("instructor_dashboard")

    else:
        form = ModuleForm()

    return render(request, "instructor/add_module.html", {
        "form": form
    })


# =====================================
# ADD LESSON
# =====================================
@login_required
def add_lesson(request, module_id):

    module = get_object_or_404(Module, id=module_id)

    if request.user != module.course.tutor.user:
        return redirect("home")

    if request.method == "POST":
        form = LessonForm(request.POST, request.FILES)

        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = module
            lesson.save()

            return redirect("instructor_dashboard")

    else:
        form = LessonForm()

    return render(request, "instructor/add_lesson.html", {
        "form": form
    })


# =====================================
# ENROLL COURSE
# =====================================
@login_required
def enroll_course(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    # Prevent tutor enrolling
    if request.user == course.tutor.user:
        return redirect('home')

    # Prevent duplicate enrollment
    if not course.students.filter(id=request.user.id).exists():
        course.students.add(request.user)

    return redirect('student_courses')


# =====================================
# STUDENT DASHBOARD
# =====================================
@login_required
def student_courses(request):

    courses = Course.objects.filter(
        students=request.user
    ).select_related('tutor')

    return render(request, "student/my_courses.html", {
        "courses": courses
    })


# =====================================
# COURSE DETAIL + PROGRESS ⭐⭐⭐
# =====================================
@login_required
def course_detail(request, pk):

    course = get_object_or_404(Course, pk=pk)

    is_tutor = request.user == course.tutor.user
    is_student = course.students.filter(id=request.user.id).exists()

    if not (is_tutor or is_student):
        return redirect("home")

    modules = course.modules.prefetch_related('lessons').all().order_by("order")

    # ✅ TOTAL LESSONS
    total_lessons = Lesson.objects.filter(
        module__course=course
    ).count()

    # ✅ COMPLETED LESSONS
    completed_lessons = LessonProgress.objects.filter(
        student=request.user,
        lesson__module__course=course,
        completed=True
    ).count()

    # ✅ PROGRESS %
    progress = 0
    if total_lessons > 0:
        progress = int((completed_lessons / total_lessons) * 100)

    # ✅ NEXT LESSON (Continue Learning)
    next_lesson = Lesson.objects.filter(
        module__course=course
    ).exclude(
        lessonprogress__student=request.user
    ).order_by('order').first()

    return render(
        request,
        "student/course_detail.html",
        {
            "course": course,
            "modules": modules,
            "progress": progress,
            "next_lesson": next_lesson
        }
    )


# =====================================
# LESSON DETAIL + AUTO COMPLETE ⭐⭐⭐
# =====================================
@login_required
def lesson_detail(request, pk):

    lesson = get_object_or_404(Lesson, pk=pk)
    course = lesson.module.course

    is_tutor = request.user == course.tutor.user
    is_student = course.students.filter(id=request.user.id).exists()

    if not (is_tutor or is_student):
        return redirect("home")

    # ✅ AUTO MARK LESSON COMPLETE
    if is_student:
        LessonProgress.objects.get_or_create(
            student=request.user,
            lesson=lesson,
            defaults={'completed': True}
        )

    return render(
        request,
        "student/lesson_detail.html",
        {"lesson": lesson}
    )
