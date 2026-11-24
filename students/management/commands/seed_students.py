from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand

from students.models import AcademicBackground, Guardian, SchoolClass, Student


class Command(BaseCommand):
    help = "Create sample classes and students for trying out the profile view."

    def handle(self, *args, **options):
        newton, _ = SchoolClass.objects.get_or_create(name="Grade 10 - Newton", defaults={"adviser": "Ms. Reyes"})
        curie, _ = SchoolClass.objects.get_or_create(name="Grade 10 - Curie", defaults={"adviser": "Mr. Santos"})

        data = [
            ("2026-0001", newton, "Maria", "Clara", "Dela Cruz", date(2010, 3, 14), "F", "enrolled",
             "Brgy. Real, Calamba, Laguna", "0917 555 0101", "maria.delacruz@example.com", "Mild asthma.",
             ("Santa Rosa Elementary School", "Grade 6", 2022, "92.50", "With Honors"),
             [("Elena Dela Cruz", "Mother", "Nurse", "0917 555 0102", True),
              ("Roberto Dela Cruz", "Father", "Driver", "0917 555 0103", False)]),
            ("2026-0002", newton, "Juan", "Miguel", "Bautista", date(2009, 11, 2), "M", "enrolled",
             "Brgy. Parian, Calamba, Laguna", "0918 555 0201", "", "",
             ("Calamba Central School", "Grade 9", 2025, "88.10", ""),
             [("Lourdes Bautista", "Mother", "Teacher", "0918 555 0202", True)]),
            ("2026-0003", curie, "Angelica", "", "Mendoza", date(2010, 7, 21), "F", "pending",
             "Brgy. Canlubang, Calamba, Laguna", "0920 555 0301", "angelica.m@example.com", "Allergic to peanuts.",
             ("St. Mary's Academy", "Grade 9", 2025, "95.00", "First Honors"),
             [("Carlos Mendoza", "Father", "Engineer", "0920 555 0302", True)]),
        ]

        for (num, klass, fn, mn, ln, bd, sex, status, addr, phone, email, med, acad, guardians) in data:
            s, created = Student.objects.get_or_create(
                student_number=num,
                defaults=dict(
                    school_class=klass, first_name=fn, middle_name=mn, last_name=ln,
                    birth_date=bd, sex=sex, status=status, address=addr,
                    contact_number=phone, email=email, medical_notes=med,
                    date_enrolled=date(2026, 6, 1) if status == "enrolled" else None,
                ),
            )
            if created:
                AcademicBackground.objects.create(
                    student=s, previous_school=acad[0], last_grade_completed=acad[1],
                    year_completed=acad[2], general_average=Decimal(acad[3]), honors=acad[4],
                )
                for g in guardians:
                    Guardian.objects.create(
                        student=s, name=g[0], relationship=g[1], occupation=g[2],
                        contact_number=g[3], is_primary=g[4],
                    )
        self.stdout.write(self.style.SUCCESS("Sample students created."))
