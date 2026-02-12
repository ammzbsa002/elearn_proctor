from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache, cache_control
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
import random, time

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
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect("login")

        user = authenticate(
            request,
            username=user_obj.username,
            password=password
        )

        if user is None:
            messages.error(request, "Invalid email or password")
            return redirect("login")

        login(request, user)

        if user.role == "admin":
            return redirect("admin_dashboard")
        elif user.role == "instructor":
            return redirect("instructor_dashboard")
        return redirect("student_dashboard")

    return render(request, "accounts/login.html")


# ==================================================
# REGISTER + SEND OTP (SESSION BASED)
# ==================================================



def register_view(request):

    if request.method == "POST":

        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password")
        role = request.POST.get("role", "student")
        reg_no = request.POST.get("registration_number", "").strip()

        # VALIDATION
        if not full_name or not email or not password or not reg_no:
            messages.error(request, "Please fill all required fields.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        if User.objects.filter(registration_number=reg_no).exists():
            messages.error(request, "Registration number already exists.")
            return redirect("register")

        # GENERATE OTP
        otp = str(random.randint(100000, 999999))

        # STORE IN SESSION
        request.session["reg_otp"] = otp
        request.session["reg_otp_time"] = time.time()

        request.session["reg_data"] = {
            "full_name": full_name,
            "email": email,
            "password": password,
            "role": role,
            "registration_number": reg_no,
        }

        request.session.modified = True

        # SEND EMAIL
        send_mail(
            subject="E-Learn OTP Verification",
            message=f"Your OTP is {otp}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        print("OTP SENT:", otp)

        messages.success(request, "OTP sent to your email.")
        return redirect("verify_otp")

    return render(request, "accounts/register.html")

# ==================================================
def verify_otp(request):

    if "reg_data" not in request.session:
        messages.error(request, "Session expired. Register again.")
        return redirect("register")

    if request.method == "POST":

        entered_otp = request.POST.get("otp", "").strip()
        session_otp = request.session.get("reg_otp")

        print("ENTERED:", entered_otp)
        print("SESSION:", session_otp)

        # ⏱ 5 minutes expiry
        if time.time() - request.session.get("reg_otp_time", 0) > 300:
            request.session.clear()
            messages.error(request, "OTP expired.")
            return redirect("register")

        if entered_otp == session_otp:

            data = request.session["reg_data"]

            User.objects.create_user(
                username=data["email"],
                email=data["email"],
                password=data["password"],
                role=data["role"],
                full_name=data["full_name"],
                registration_number=data["registration_number"],  # ⭐ IMPORTANT
            )


            request.session.clear()

            messages.success(request, "Registration successful. Login now.")
            return redirect("login")

        messages.error(request, "Invalid OTP.")

    return render(request, "accounts/verify_otp.html")


# ==================================================
# PASSWORD RESET (SESSION BASED)
# ==================================================

def password_recovery(request):
    return render(request, "accounts/password_recovery.html")

def verify_otp(request):

    if "reg_data" not in request.session:
        messages.error(request, "Session expired. Please register again.")
        return redirect("register")

    if request.method == "POST":

        entered_otp = request.POST.get("otp", "").strip()
        session_otp = request.session.get("reg_otp")

        print("ENTERED:", entered_otp)
        print("SESSION:", session_otp)

        # OTP expiry (5 minutes)
        if time.time() - request.session.get("reg_otp_time", 0) > 300:
            request.session.flush()
            messages.error(request, "OTP expired.")
            return redirect("register")

        # MATCH OTP
        if entered_otp == session_otp:

            data = request.session.get("reg_data")

            try:
                User.objects.create_user(
                    username=data["email"],
                    email=data["email"],
                    password=data["password"],
                    role=data["role"],
                    full_name=data["full_name"],
                    registration_number=data["registration_number"],
                )

            except Exception as e:
                messages.error(request, "User creation failed. Try again.")
                print("CREATE USER ERROR:", e)
                return redirect("register")

            # CLEAR SESSION
            request.session.flush()

            messages.success(request, "Registration successful. Please login.")
            return redirect("login")

        else:
            messages.error(request, "Invalid OTP.")

    return render(request, "accounts/verify_otp.html")

# ==================================================
# DASHBOARDS
# ==================================================
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def student_dashboard(request):

    enrolled_courses = Course.objects.filter(
        students=request.user
    ).select_related('tutor')

    print("LOGGED USER:", request.user)
    print("ENROLLED COURSES:", enrolled_courses)

    return render(request, "dashboards/student_dashboard.html", {
        "courses": enrolled_courses
    })



@login_required
def instructor_dashboard(request):
    return render(request, "dashboards/instructor_dashboard.html")


@login_required
def admin_dashboard(request):
    return render(request, "dashboards/admin_dashboard.html")


# ==================================================
# LOGOUT
# ==================================================
def logout_view(request):
    logout(request)
    return redirect("home")
