from django.contrib import admin
from .models import Doctor, Patient, Appointment
# Register your models here.

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'specialization', 'phone', 'email', 'created_at', 'updated_at')
    search_fields = ('name', 'specialization', 'email', 'phone')
    list_filter = ('specialization', 'created_at', 'updated_at')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'address', 'date_of_birth', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('date_of_birth', 'created_at', 'updated_at')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'created_at', 'updated_at')
    search_fields = ('patient__name', 'doctor__name', 'description')
    list_filter = ('status', 'appointment_date', 'doctor', 'created_at', 'updated_at')
