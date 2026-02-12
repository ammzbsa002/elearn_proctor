from django.db import models
from courses.models import Course


class Assignment(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="assignments"
    )

    title = models.CharField(max_length=255)

    instructions = models.TextField()   # ✅ ADD THIS

    due_date = models.DateTimeField()

    total_marks = models.IntegerField(default=100)   # ✅ ADD THIS

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
