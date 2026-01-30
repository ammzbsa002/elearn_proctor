from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),

    # ✅ DASHBOARDS (THIS FIXES YOUR ERROR)
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('instructor/dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path("password-recovery/", views.password_recovery, name="password_recovery"),

]
