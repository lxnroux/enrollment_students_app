from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="students:list")),
    path("admin/", admin.site.urls),
    path("students/", include("students.urls")),
]