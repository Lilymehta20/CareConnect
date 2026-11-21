from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, DoctorProfile, Appointment, Prescription, Feedback

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone", "role", "password1", "password2")

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        exclude = ("user", "is_verified")
        widgets = {"bio": forms.Textarea(attrs={"rows": 3}), "address": forms.Textarea(attrs={"rows": 2})}

class AppointmentForm(forms.ModelForm):
    appointment_at = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    class Meta:
        model = Appointment
        fields = ("appointment_at", "reason")

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ("diagnosis", "medicines", "instructions")

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ("rating", "comment")
        widgets = {"rating": forms.Select(choices=[(i, f"{i}/5") for i in range(1, 6)])}
