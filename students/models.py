from datetime import date

from django.db import models


class SchoolClass(models.Model):
    """A class/section that students are enrolled in."""
    name = models.CharField(max_length=60)              # e.g. "Grade 10 - Newton"
    adviser = models.CharField(max_length=100, blank=True)
    school_year = models.CharField(max_length=9, default="2026-2027")

    class Meta:
        verbose_name_plural = "school classes"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.school_year})"


class Student(models.Model):
    class Status(models.TextChoices):
        ENROLLED = "enrolled", "Enrolled"
        PENDING = "pending", "Pending"
        DROPPED = "dropped", "Dropped"

    class Sex(models.TextChoices):
        FEMALE = "F", "Female"
        MALE = "M", "Male"

    # Enrollment info
    student_number = models.CharField(max_length=20, unique=True)
    school_class = models.ForeignKey(
        SchoolClass, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="students",
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    date_enrolled = models.DateField(null=True, blank=True)

    # Personal info
    first_name = models.CharField(max_length=60)
    middle_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=60)
    birth_date = models.DateField()
    sex = models.CharField(max_length=1, choices=Sex.choices)
    address = models.TextField(blank=True)
    contact_number = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)

    # Health / emergency
    medical_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.last_name}, {self.first_name} {self.middle_name}".strip()

    @property
    def display_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def initials(self):
        return f"{self.first_name[:1]}{self.last_name[:1]}".upper()

    @property
    def age(self):
        today = date.today()
        b = self.birth_date
        return today.year - b.year - ((today.month, today.day) < (b.month, b.day))


class Guardian(models.Model):
    """Family background: parents / guardians of a student."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="guardians")
    name = models.CharField(max_length=120)
    relationship = models.CharField(max_length=40)      # Mother, Father, Aunt...
    occupation = models.CharField(max_length=100, blank=True)
    contact_number = models.CharField(max_length=30, blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ["-is_primary", "name"]

    def __str__(self):
        return f"{self.name} ({self.relationship})"


class AcademicBackground(models.Model):
    """Previous school records of a student."""
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="academic")
    previous_school = models.CharField(max_length=150, blank=True)
    last_grade_completed = models.CharField(max_length=40, blank=True)
    year_completed = models.PositiveIntegerField(null=True, blank=True)
    general_average = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    honors = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return f"Academic background of {self.student}"
