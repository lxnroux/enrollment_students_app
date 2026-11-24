from django.contrib import admin

from .models import AcademicBackground, Guardian, SchoolClass, Student


class GuardianInline(admin.TabularInline):
    model = Guardian
    extra = 1


class AcademicInline(admin.StackedInline):
    model = AcademicBackground


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_number", "full_name", "school_class", "status")
    list_filter = ("status", "school_class")
    search_fields = ("first_name", "last_name", "student_number")
    inlines = [AcademicInline, GuardianInline]


admin.site.register(SchoolClass)
