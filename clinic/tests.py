from django.test import TestCase
from django.urls import reverse

from .models import Appointment, DoctorProfile, Prescription, User


class PrescriptionTests(TestCase):
    def setUp(self):
        self.doctor = User.objects.create_user(
            username="doctor",
            password="test-password",
            role=User.DOCTOR,
        )
        self.profile = DoctorProfile.objects.create(
            user=self.doctor,
            specialization="Cardiology",
            is_verified=True,
        )
        self.patient = User.objects.create_user(
            username="patient",
            password="test-password",
            role=User.PATIENT,
        )
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.profile,
            appointment_at="2027-01-01T10:00:00+05:30",
            status="accepted",
        )

    def test_doctor_can_add_prescription(self):
        self.client.force_login(self.doctor)
        response = self.client.post(
            reverse("add_prescription", args=[self.appointment.id]),
            {
                "diagnosis": "Mild hypertension",
                "medicines": "Medicine A - once daily",
                "instructions": "Recheck in two weeks",
            },
        )

        self.assertRedirects(response, reverse("dashboard"))
        prescription = Prescription.objects.get(appointment=self.appointment)
        self.assertEqual(prescription.diagnosis, "Mild hypertension")
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, "completed")

    def test_completed_appointment_can_edit_prescription(self):
        prescription = Prescription.objects.create(
            appointment=self.appointment,
            diagnosis="Old diagnosis",
            medicines="Old medicine",
            instructions="",
        )
        self.appointment.status = "completed"
        self.appointment.save(update_fields=["status"])
        self.client.force_login(self.doctor)

        response = self.client.post(
            reverse("add_prescription", args=[self.appointment.id]),
            {
                "diagnosis": "Updated diagnosis",
                "medicines": "Updated medicine",
                "instructions": "Updated instructions",
            },
        )

        self.assertRedirects(response, reverse("dashboard"))
        prescription.refresh_from_db()
        self.assertEqual(prescription.diagnosis, "Updated diagnosis")
