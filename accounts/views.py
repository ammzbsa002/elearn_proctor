from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings


import random
import re

from courses.models import Course

User = get_user_model()

# ==================================================
# HOME
# ==================================================
def home(request):
    courses = Course.objects.all()
    return render(request, 'home.html', {'courses': courses})


# ==================================================
# LOGIN
# ==================================================
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect('login')

        user = authenticate(
            request,
            username=user.username,
            password=password
        )

        if user is None:
            messages.error(request, "Invalid email or password")
            return redirect('login')

        login(request, user)

        if user.role == 'admin':
            return redirect('admin_dashboard')
        elif user.role == 'instructor':
            return redirect('instructor_dashboard')
        else:
            return redirect('student_dashboard')

    return render(request, "accounts/login.html")

# ==================================================
# REGISTER (OTP + ALL FIELDS ENABLED)
# ==================================================
def register_view(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name").strip()
        degree = request.POST.get("degree").strip()
        reg_no = request.POST.get("registration_number").strip().upper()
        mobile = request.POST.get("mobile").strip()
        email = request.POST.get("email").strip().lower()
        college = request.POST.get("college_name").strip()
        password = request.POST.get("password")
        role = request.POST.get("role", "student")

        # ---------------- VALIDATIONS ----------------
        if not re.match(r'^[A-Za-z\s]+$', full_name):
            messages.error(request, "Name should contain only letters")
            return redirect('register')

        if not re.fullmatch(r'[6-9]\d{9}', mobile):
            messages.error(request, "Enter valid 10-digit mobile number")
            return redirect('register')

        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            messages.error(request, "Enter a valid email address")
            return redirect('register')

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        if User.objects.filter(registration_number__iexact=reg_no).exists():
            messages.error(request, "Registration number already exists")
            return redirect('register')

        # ---------------- OTP GENERATION ----------------
        otp = random.randint(100000, 999999)

        # ---------------- STORE IN SESSION ----------------
        request.session['reg_otp'] = str(otp)
        request.session['reg_data'] = {
            'full_name': full_name,
            'degree': degree,
            'registration_number': reg_no,
            'mobile': mobile,
            'email': email,
            'college_name': college,
            'password': password,
            'role': role
        }

        # ---------------- SEND OTP EMAIL ----------------
        send_mail(
            subject="E-Learn Proctor | Registration OTP",
            message=f"""
Hello {full_name},

Your OTP for account registration is:

{otp}

This OTP is valid for 5 minutes.
Do not share it with anyone.

Regards,
E-Learn Proctor Team
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        print("REG OTP:", otp)  # backup (terminal)
        messages.success(request, "OTP has been sent to your email")
        return redirect('verify_otp')

    return render(request, 'accounts/login.html')

def verify_otp(request):
    masked_email = ""

    if 'reg_data' in request.session:
        email = request.session['reg_data'].get('email', '')
        if email and '@' in email:
            name, domain = email.split('@')
            masked_email = name[:3] + '*****@' + domain

    if request.method == "POST":
        entered_otp = request.POST.get("otp", "").strip()

        if 'reg_otp' not in request.session:
            messages.error(request, "Session expired. Please register again.")
            return redirect('register')

        if entered_otp == request.session.get('reg_otp'):
            data = request.session.get('reg_data')

            User.objects.create_user(
                username=data['email'],
                email=data['email'],
                password=data['password'],
                role=data['role'],
                full_name=data['full_name'],
                degree=data.get('degree', ''),
                registration_number=data['registration_number'],
                mobile=data['mobile'],
                college_name=data['college_name']
            )

            request.session.flush()
            messages.success(request, "Registration successful. Please login.")
            return redirect('login')

        messages.error(request, "Invalid OTP")

    return render(request, 'accounts/verify_otp.html', {
        'masked_email': masked_email
    })




import time

def password_recovery(request):
    step = "email"
    reset_done = False

    # ---------- SEND OTP ----------
    if request.method == "POST" and "email" in request.POST:
        email = request.POST.get("email").strip().lower()

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email not registered")
            return render(request, "accounts/password_recovery.html", {"step": "email"})

        otp = random.randint(100000, 999999)

        request.session["reset_email"] = email
        request.session["reset_otp"] = str(otp)
        request.session["otp_time"] = time.time()   # ⏱ store time

        send_mail(
            subject="Password Reset OTP - E-Learn Proctor",
            message=f"Your OTP is {otp}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        messages.success(request, "OTP sent to your email")
        step = "otp"

    # ---------- VERIFY OTP ----------
    elif request.method == "POST" and "otp" in request.POST:
        entered_otp = request.POST.get("otp")
        new_password = request.POST.get("password")

        if "reset_otp" not in request.session:
            messages.error(request, "Session expired. Try again.")
            return redirect("password_recovery")

        # ⏱ OTP expiry (2 minutes)
        if time.time() - request.session.get("otp_time", 0) > 120:
            messages.error(request, "OTP expired. Please resend OTP.")
            step = "otp"

        elif entered_otp == request.session["reset_otp"]:
            user = User.objects.get(email=request.session["reset_email"])
            user.set_password(new_password)
            user.save()

            request.session.flush()
            messages.success(request, "Password reset successful")
            reset_done = True
            step = "otp"

        else:
            messages.error(request, "Invalid OTP")
            step = "otp"

    return render(
        request,
        "accounts/password_recovery.html",
        {
            "step": step,
            "reset_done": reset_done
        }
    )



# ==================================================
# DASHBOARDS
# ==================================================
@login_required
def student_dashboard(request):
    return render(request, 'dashboards/student_dashboard.html')


@login_required
def instructor_dashboard(request):
    return render(request, 'dashboards/instructor_dashboard.html')


@login_required
def admin_dashboard(request):
    return render(request, 'dashboards/admin_dashboard.html')


# ==================================================
# COURSE DETAIL
# ==================================================
def course_detail(request, id):
    course = get_object_or_404(Course, id=id)
    contents = course.contents.all().order_by('order')
    return render(request, 'course_detail.html', {
        'course': course,
        'contents': contents
    })
