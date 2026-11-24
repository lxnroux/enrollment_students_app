from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import SchoolClass, Student


def student_profiles(request, pk=None):
    """Student list on the left; the clicked student's profile on the right."""
    students = Student.objects.select_related("school_class")

    q = request.GET.get("q", "").strip()
    class_id = request.GET.get("class", "")

    if q:
        students = students.filter(
            Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(student_number__icontains=q)
        )
    if class_id.isdigit():
        students = students.filter(school_class_id=class_id)

    selected = None
    if pk is not None:
        selected = get_object_or_404(
            Student.objects.select_related("school_class", "academic")
            .prefetch_related("guardians"),
            pk=pk,
        )

    return render(request, "students/index.html", {
        "students": students,
        "selected": selected,
        "classes": SchoolClass.objects.all(),
        "q": q,
        "class_id": class_id,
    })
