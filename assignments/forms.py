from django import forms
from .models import Assignment, Question


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = [
            'course',
            'title',
            'instructions',
            'due_date',
            'total_marks'
        ]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'question_text',
            'option_a',
            'option_b',
            'option_c',
            'option_d',
            'correct_answer'
        ]
