from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="clinic/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("doctor/profile/", views.doctor_profile, name="doctor_profile"),
    path("doctors/", views.doctor_search, name="doctor_search"),
    path("doctors/<int:doctor_id>/book/", views.book_appointment, name="book_appointment"),
    path("appointments/<int:appointment_id>/prescription/", views.add_prescription, name="add_prescription"),
    path("appointments/<int:appointment_id>/<str:status>/", views.update_appointment, name="update_appointment"),
    path("records/", views.records, name="records"),
    path("doctors/<int:doctor_id>/feedback/", views.feedback, name="feedback"),
]
