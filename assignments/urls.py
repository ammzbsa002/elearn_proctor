from django.urls import path
from .views import instructor_assignments

app_name = "assignments"   # ⭐ IMPORTANT

urlpatterns = [

    path("manage/", instructor_assignments, name="instructor_assignments"),
    

]
