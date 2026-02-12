from django.contrib import admin
from .models import Tutor, Course, Module, Lesson, LessonProgress

admin.site.register(Tutor)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(LessonProgress)
