from django.db import models
from django.conf import settings


# ================= TUTOR =================
class Tutor(models.Model):
    user = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
)


    qualification = models.CharField(max_length=200)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='tutors/')

    def __str__(self):
        return self.user.username


# ================= COURSE =================
class Course(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='courses')

    title = models.CharField(max_length=200)
    description = models.TextField()

    level = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)

    image = models.ImageField(upload_to='courses/')
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ ENROLLMENT FEATURE
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='enrolled_courses',
        blank=True
    )

    def __str__(self):
        return self.title


# ================= MODULE =================
class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')

    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.course.title} - {self.title}"


# ================= LESSON =================
class Lesson(models.Model):

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='lessons'
    )

    title = models.CharField(max_length=200)

    # ⭐ Accept ANY YouTube link
    video_url = models.URLField(blank=True, null=True)

    # ⭐ Upload PDFs / notes
    notes_file = models.FileField(
        upload_to='lesson_notes/',
        blank=True,
        null=True
    )

    content = models.TextField(blank=True)

    order = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


    # ⭐ AUTO-CONVERT YOUTUBE LINK
    def get_embed_url(self):

        if self.video_url:

            if "watch?v=" in self.video_url:
                return self.video_url.replace("watch?v=", "embed/")

            if "youtu.be" in self.video_url:
                video_id = self.video_url.split("/")[-1]
                return f"https://www.youtube.com/embed/{video_id}"

        return self.video_url


# ================= PROGRESS TRACKING =================
class LessonProgress(models.Model):

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    completed = models.BooleanField(default=False)

    completed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student} - {self.lesson}"
