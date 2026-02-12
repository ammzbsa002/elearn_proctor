from django import forms
from .models import Course, Module, Lesson


# ================= COURSE =================
from django.forms import CheckboxSelectMultiple

# ================= COURSE =================
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course

        
        fields = [
            'title',
            'description',
            'level',
            'duration',
            'image'
        ]

        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Enter course description...'
            }),
        }


# ================= MODULE =================
class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'order']


# ================= LESSON =================
class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = [
            'title',
            'video_url',
            'notes_file',
            'content',
            'order'
        ]

        widgets = {

            'content': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Optional lesson explanation...'
            }),

            'order': forms.NumberInput(attrs={
                'min': 1
            }),

            'video_url': forms.URLInput(attrs={
                'placeholder': 'Paste YouTube link here'
            })
        }

        labels = {
            'video_url': 'YouTube Link',
            'notes_file': 'Upload Notes (PDF)',
        }

    def clean(self):
        cleaned_data = super().clean()

        video = cleaned_data.get("video_url")
        notes = cleaned_data.get("notes_file")
        content = cleaned_data.get("content")

        if not video and not notes and not content:
            raise forms.ValidationError(
                "Add at least ONE: Video, Notes, or Lesson Content."
            )

        return cleaned_data
