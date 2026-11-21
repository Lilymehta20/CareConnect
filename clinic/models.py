from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    PATIENT = "patient"
    DOCTOR = "doctor"
    ROLE_CHOICES = [(PATIENT, "Patient"), (DOCTOR, "Doctor")]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=PATIENT)
    phone = models.CharField(max_length=20, blank=True)

class DoctorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor_profile")
    specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=150, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    clinic_name = models.CharField(max_length=150, blank=True)
    address = models.TextField(blank=True)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name() or self.user.username} — {self.specialization}"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"), ("accepted", "Accepted"),
        ("completed", "Completed"), ("cancelled", "Cancelled"),
    ]
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patient_appointments")
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="appointments")
    appointment_at = models.DateTimeField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-appointment_at"]

    def __str__(self):
        return f"{self.patient} with {self.doctor} ({self.appointment_at:%Y-%m-%d %H:%M})"

class MedicalRecord(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="medical_records")
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=160)
    notes = models.TextField(blank=True)
    attachment = models.FileField(upload_to="medical_records/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="prescription")
    diagnosis = models.TextField()
    medicines = models.TextField(help_text="Enter medicine, dosage and duration")
    instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="feedback")
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
