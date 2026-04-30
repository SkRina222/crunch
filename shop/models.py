from django.db import models

# lab 5: крок 1 - додано модель Service для послуг та пов'язано Appointment -> Service
# lab 6: крок 1 - додано поле image до моделі Service для фотографій послуг; крок 9 - додано поля rating (DecimalField для рейтингу лікаря від 0.0 до 5.0) та procedures (ManyToManyField до Service для процедур, які проводить лікар) до моделі Doctor
class Doctor(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=255, verbose_name="Ім'я")
    specialization = models.CharField(max_length=255, verbose_name="Спеціалізація")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    photo = models.ImageField(blank=True, null=True, upload_to='doctors/', verbose_name='Фото')
    # lab 6: крок 9 - додано поле procedures як ManyToManyField до Service для зв'язку лікарів з процедурами
    procedures = models.ManyToManyField('Service', blank=True, related_name='doctors', verbose_name="Процедури")
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

class Service(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=255, verbose_name="Назва")
    description = models.TextField(verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    duration = models.PositiveIntegerField(verbose_name="Тривалість (хв)", help_text="Тривалість послуги в хвилинах")
    image = models.ImageField(blank=True, null=True, upload_to='services/', verbose_name='Фото')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")
    
    class Meta:
        verbose_name = "Послуга"
        verbose_name_plural = "Послуги"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Appointment(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments', verbose_name="Пацієнт")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments', verbose_name="Лікар")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments', verbose_name="Послуга", default=1)
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
        return f"{self.patient.name} - {self.doctor.name} - {self.service.name}"