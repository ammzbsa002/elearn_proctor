from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

from django.conf import settings
from django.conf.urls.static import static


def home(request):
    return render(request, 'home.html')


# ✅ CREATE urlpatterns FIRST
urlpatterns = [

    path('admin/', admin.site.urls),

    path('', home, name='home'),

    path('', include('accounts.urls')),

    path('courses/', include('courses.urls')),

    path('assignments/', include('assignments.urls')),
]


# ✅ ADD MEDIA ONLY AFTER urlpatterns EXISTS
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
