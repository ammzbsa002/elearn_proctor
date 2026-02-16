from django.db import models

class Assignment(models.Model):

    course = models.ForeignKey(
        "courses.Course",   # ✅ string reference
        on_delete=models.CASCADE,
        related_name="assignments"
    )

    title = models.CharField(max_length=255)
    instructions = models.TextField()
    due_date = models.DateTimeField()
    total_marks = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):

    ANSWER_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]

    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)

    correct_answer = models.CharField(
        max_length=1,
        choices=ANSWER_CHOICES
    )

    def __str__(self):
        return self.question_text
