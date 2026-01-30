from django.shortcuts import render

# Create your views here.
from courses.models import Course

def home(request):
    courses = Course.objects.order_by('-rating')[:6]
    return render(request, 'home.html', {'courses': courses})
