from django.urls import path
from . import views


app_name = "accounts"
urlpatterns = [
    path("user_update", views.user_update, name="user-update"),
    path("user_profile", views.user_profile, name="user-profile"),
    path("new_patient", views.new_patient, name="new-patient"),
    path("new_doctor", views.new_doctor, name="new-doctor"),
    path("new_staff", views.user_doctor_profile, name="user-doctor-profile"),
]
