
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('instructor', 'Instructor'),
        ('student', 'Student'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )

    full_name = models.CharField(max_length=150, default='')
    degree = models.CharField(max_length=100, default='')

    registration_number = models.CharField(
    max_length=50,
    unique=True,
    null=True,
    blank=True
)


    mobile = models.CharField(max_length=10, default='')
    registration_number = models.CharField(
    max_length=50,
    unique=True,
    blank=False,
    null=False
)


    email = models.EmailField(max_length=191, unique=True)

    college_name = models.CharField(max_length=200, default='')  # 👈 FIX HERE

    def __str__(self):
        return f"{self.username} ({self.role})"