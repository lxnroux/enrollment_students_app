# Enrollment System – Student Profile View (Step 1)

## Setup
```bash
pip install django
django-admin startproject config .        # skip if you already have a project
# copy the `students/` folder next to manage.py
```

1. In `config/settings.py` add `"students"` to `INSTALLED_APPS`.
2. In `config/urls.py`:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("students/", include("students.urls")),
]
```
3. Run:
```bash
python manage.py makemigrations students
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_students      # optional sample data
python manage.py runserver
```
Open http://127.0.0.1:8000/students/ and click a student.
Add or edit students at http://127.0.0.1:8000/admin/.
