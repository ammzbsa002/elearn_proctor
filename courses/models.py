

# Create your models here.
from django.db import models


# ================= TUTOR MODEL =================
class Tutor(models.Model):
    name = models.CharField(max_length=150)
    qualification = models.CharField(max_length=200)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='tutors/')

    def __str__(self):
        return self.name


# ================= COURSE MODEL =================
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    level = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    rating = models.FloatField(default=0)

    image = models.ImageField(upload_to='courses/')
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# ================= COURSE CONTENT MODEL =================
class CourseContent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='contents')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField()

    def __str__(self):
        return f"{self.course.title} - {self.title}"

