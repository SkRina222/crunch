from django.db import models

class Doctor(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=255, verbose_name="Ім'я")
    specialization = models.CharField(max_length=255, verbose_name="Спеціалізація")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")
    
    class Meta:
        verbose_name = "Лікар"
        verbose_name_plural = "Лікарі"
        ordering = ['name']
        
    
    def __str__(self):
        return self.name
    
class Patient(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=255, verbose_name="Ім'я")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    address = models.TextField(blank=True, null=True, verbose_name="Адреса")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Дата народження")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")
    
    class Meta:
        verbose_name = "Пацієнт"
        verbose_name_plural = "Пацієнти"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Appointment(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments', verbose_name="Пацієнт")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments', verbose_name="Лікар")
    appointment_date = models.DateField(verbose_name="Дата запису")
    appointment_time = models.TimeField(verbose_name="Час запису")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")
    status = models.CharField(max_length=50, choices=[
        ('scheduled', 'Запланований'),
        ('completed', 'Завершений'),
        ('cancelled', 'Скасований')
    ], default='scheduled', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")
    
    class Meta: 
        verbose_name = "Запис"
        verbose_name_plural = "Записи"
        ordering = ['appointment_date', 'appointment_time']

    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name}"
