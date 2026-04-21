from django.contrib import admin
<<<<<<< HEAD
from .models import Doctor, Patient, Service, Appointment
# lab 5: крок 2 - зареєстровано моделі в адмінці: Doctor, Patient, Service, Appointment
=======
from .models import Doctor, Patient, Appointment
>>>>>>> 67b9306e19dd59a2420b989b829b2d252a67a97a
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

<<<<<<< HEAD
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'duration', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('price', 'duration', 'created_at', 'updated_at')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'service', 'appointment_date', 'appointment_time', 'status', 'created_at', 'updated_at')
    search_fields = ('patient__name', 'doctor__name', 'service__name', 'description')
    list_filter = ('status', 'appointment_date', 'doctor', 'service', 'created_at', 'updated_at')
=======
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'created_at', 'updated_at')
    search_fields = ('patient__name', 'doctor__name', 'description')
    list_filter = ('status', 'appointment_date', 'doctor', 'created_at', 'updated_at')
>>>>>>> 67b9306e19dd59a2420b989b829b2d252a67a97a
