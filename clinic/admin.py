from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, DoctorProfile, Appointment, MedicalRecord, Prescription, Feedback

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("CareConnect", {"fields": ("role", "phone")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("CareConnect", {"fields": ("role", "phone")}),)

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "specialization", "clinic_name", "is_verified", "is_available")
    list_filter = ("is_verified", "specialization")
    search_fields = ("user__username", "user__first_name", "specialization")
    list_editable = ("is_verified", "is_available")

admin.site.register(Appointment)
admin.site.register(MedicalRecord)
admin.site.register(Prescription)
admin.site.register(Feedback)
