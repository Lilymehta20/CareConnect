from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .decorators import role_required
from .forms import RegisterForm, DoctorProfileForm, AppointmentForm, PrescriptionForm, FeedbackForm
from .models import User, DoctorProfile, Appointment, MedicalRecord, Prescription

def home(request):
    doctors = DoctorProfile.objects.filter(is_verified=True, is_available=True).select_related("user")[:6]
    return render(request, "clinic/home.html", {"doctors": doctors})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == User.DOCTOR:
                return redirect("doctor_profile")
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "clinic/form.html", {"form": form, "heading": "Create your CareConnect account"})

@login_required
def dashboard(request):
    if request.user.role == User.DOCTOR:
        profile = getattr(request.user, "doctor_profile", None)
        appointments = Appointment.objects.filter(doctor=profile) if profile else Appointment.objects.none()
        return render(request, "clinic/doctor_dashboard.html", {"profile": profile, "appointments": appointments})
    appointments = Appointment.objects.filter(patient=request.user).select_related("doctor__user")
    records = MedicalRecord.objects.filter(patient=request.user)
    return render(request, "clinic/patient_dashboard.html", {"appointments": appointments, "records": records})

@role_required(User.DOCTOR)
def doctor_profile(request):
    profile = getattr(request.user, "doctor_profile", None)
    if request.method == "POST":
        form = DoctorProfileForm(request.POST, instance=profile)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.is_verified = False
            obj.save()
            messages.success(request, "Profile saved. An administrator must verify it before it appears in search.")
            return redirect("dashboard")
    else:
        form = DoctorProfileForm(instance=profile)
    return render(request, "clinic/form.html", {"form": form, "heading": "Doctor profile"})

def doctor_search(request):
    query = request.GET.get("q", "").strip()
    doctors = DoctorProfile.objects.filter(is_verified=True, is_available=True).select_related("user")
    if query:
        doctors = doctors.filter(Q(specialization__icontains=query) | Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query) | Q(clinic_name__icontains=query))
    return render(request, "clinic/doctor_search.html", {"doctors": doctors, "query": query})

@role_required(User.PATIENT)
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, pk=doctor_id, is_verified=True, is_available=True)
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = doctor
            if appointment.appointment_at <= timezone.now():
                form.add_error("appointment_at", "Choose a future date and time.")
            else:
                appointment.save()
                messages.success(request, "Appointment request sent to the doctor.")
                return redirect("dashboard")
    else:
        form = AppointmentForm()
    return render(request, "clinic/form.html", {"form": form, "heading": f"Book appointment with Dr. {doctor.user.get_full_name() or doctor.user.username}"})

@login_required
def update_appointment(request, appointment_id, status):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    is_doctor = request.user.role == User.DOCTOR and getattr(request.user, "doctor_profile", None) == appointment.doctor
    is_patient_cancel = request.user == appointment.patient and status == "cancelled"
    if not (is_doctor or is_patient_cancel):
        raise PermissionDenied
    allowed = ["accepted", "completed"] if is_doctor else ["cancelled"]
    if request.method == "POST" and status in allowed:
        appointment.status = status
        appointment.save(update_fields=["status"])
        messages.success(request, f"Appointment marked {status}.")
    return redirect("dashboard")

@role_required(User.DOCTOR)
def add_prescription(request, appointment_id):
    profile = get_object_or_404(DoctorProfile, user=request.user)
    appointment = get_object_or_404(Appointment, pk=appointment_id, doctor=profile, status__in=["accepted", "completed"])
    try:
        instance = appointment.prescription
    except Prescription.DoesNotExist:
        instance = None
    if request.method == "POST":
        form = PrescriptionForm(request.POST, instance=instance)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.save()
            appointment.status = "completed"
            appointment.save(update_fields=["status"])
            messages.success(request, "Prescription saved.")
            return redirect("dashboard")
    else:
        form = PrescriptionForm(instance=instance)
    return render(request, "clinic/form.html", {"form": form, "heading": "Create digital prescription"})

@login_required
def records(request):
    if request.user.role != User.PATIENT:
        raise PermissionDenied
    items = MedicalRecord.objects.filter(patient=request.user)
    prescriptions = Prescription.objects.filter(appointment__patient=request.user).select_related("appointment__doctor__user")
    return render(request, "clinic/records.html", {"records": items, "prescriptions": prescriptions})

@role_required(User.PATIENT)
def feedback(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, pk=doctor_id)
    has_completed = Appointment.objects.filter(patient=request.user, doctor=doctor, status="completed").exists()
    if not has_completed:
        raise PermissionDenied
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.patient, item.doctor = request.user, doctor
            item.save()
            messages.success(request, "Thank you for your feedback.")
            return redirect("dashboard")
    else:
        form = FeedbackForm()
    return render(request, "clinic/form.html", {"form": form, "heading": "Rate your consultation"})
