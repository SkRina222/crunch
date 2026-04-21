# Лабораторна робота №4 — Моделі та адмін-панель у Django

**Тема проєкту:** Медичний сайт — управління лікарями, пацієнтами та записами на прийом.

---

## Що потрібно було зробити

- Описати моделі (таблиці бази даних) для свого сайту — мінімум 3 таблиці
- Мінімум дві таблиці мають бути з'єднані між собою
- Налаштувати адмін-панель: відображення назви, дати створення, дати оновлення
- Додати через адмінку кілька елементів у кожну таблицю

---

## Що таке модель у Django

Модель — це Python-клас, який описує одну таблицю в базі даних. Кожен атрибут класу — це колонка таблиці. Django сам перетворює цей клас на SQL і створює таблицю.

Усі моделі описуються у файлі `shop/models.py` і успадковуються від `models.Model`.

---

## Які таблиці створено та навіщо

Проєкт має три моделі:

```
Doctor        ← лікарі клініки
Patient       ← пацієнти
Appointment   ← записи на прийом (з'єднує лікаря і пацієнта)
```

`Appointment` посилається одночасно на `Doctor` і на `Patient` — це і є з'єднання таблиць.

---

## Файл `models.py` — повний розбір

### Модель `Doctor`

```python
class Doctor(models.Model):
    id             = models.AutoField(primary_key=True, verbose_name="ID")
    name           = models.CharField(max_length=255, verbose_name="Ім'я")
    specialization = models.CharField(max_length=255, verbose_name="Спеціалізація")
    description    = models.TextField(blank=True, null=True, verbose_name="Опис")
    phone          = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    email          = models.EmailField(blank=True, null=True, verbose_name="Email")
    created_at     = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at     = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        verbose_name        = "Лікар"
        verbose_name_plural = "Лікарі"
        ordering            = ['name']

    def __str__(self):
        return self.name
```

**Що і навіщо написано:**

`id = models.AutoField(primary_key=True)` — унікальний номер кожного запису. Django додає його автоматично, але тут він прописаний вручну явно. Це головний ключ таблиці — жоден запис не може мати однаковий `id`.

`name = models.CharField(max_length=255)` — текстове поле обмеженої довжини. `max_length=255` — максимальна кількість символів. Використовується для коротких рядків: ім'я, заголовок, спеціалізація.

`description = models.TextField(blank=True, null=True)` — текст без обмеження довжини. `blank=True` означає, що поле не обов'язкове у формі. `null=True` означає, що в базі даних може зберігатись `NULL` (порожнє значення). Ці два параметри завжди вказуються разом для необов'язкових полів.

`email = models.EmailField(blank=True, null=True)` — це той самий `CharField(max_length=254)`, але Django додатково перевіряє, чи введений рядок схожий на email-адресу (містить `@`).

`created_at = models.DateTimeField(auto_now_add=True)` — дата і час створення запису. Параметр `auto_now_add=True` означає: Django сам підставить поточний час у момент створення об'єкта. Поле стає нередагованим — змінити його вручну не можна.

`updated_at = models.DateTimeField(auto_now=True)` — дата і час останнього збереження. `auto_now=True` означає: час оновлюється автоматично **при кожному збереженні** об'єкта.

`class Meta` — внутрішній клас з налаштуваннями моделі. `verbose_name` і `verbose_name_plural` — як модель відображатиметься в адмінці (в однині і множині). `ordering = ['name']` — записи за замовчуванням сортуються за іменем в алфавітному порядку.

`def __str__` — метод, який визначає текстове представлення об'єкта. Завдяки йому в адмінці замість `Doctor object (1)` буде відображатись ім'я лікаря.

---

### Модель `Patient`

```python
class Patient(models.Model):
    id            = models.AutoField(primary_key=True, verbose_name="ID")
    name          = models.CharField(max_length=255, verbose_name="Ім'я")
    email         = models.EmailField(verbose_name="Email")
    phone         = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    address       = models.TextField(blank=True, null=True, verbose_name="Адреса")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Дата народження")
    created_at    = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at    = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        verbose_name        = "Пацієнт"
        verbose_name_plural = "Пацієнти"
        ordering            = ['name']

    def __str__(self):
        return self.name
```

**Що нового порівняно з `Doctor`:**

`email = models.EmailField()` — тут немає `blank=True, null=True`. Це означає, що email є **обов'язковим** полем: без нього запис не збережеться.

`date_of_birth = models.DateField(blank=True, null=True)` — зберігає лише дату без часу (`YYYY-MM-DD`). Для дати народження час не потрібен, тому `DateField` підходить краще, ніж `DateTimeField`.

---

### Модель `Appointment` — з'єднання таблиць

```python
class Appointment(models.Model):
    id               = models.AutoField(primary_key=True, verbose_name="ID")
    patient          = models.ForeignKey(
                           Patient,
                           on_delete=models.CASCADE,
                           related_name='appointments',
                           verbose_name="Пацієнт"
                       )
    doctor           = models.ForeignKey(
                           Doctor,
                           on_delete=models.CASCADE,
                           related_name='appointments',
                           verbose_name="Лікар"
                       )
    appointment_date = models.DateField(verbose_name="Дата запису")
    appointment_time = models.TimeField(verbose_name="Час запису")
    description      = models.TextField(blank=True, null=True, verbose_name="Опис")
    status           = models.CharField(
                           max_length=50,
                           choices=[
                               ('scheduled', 'Запланований'),
                               ('completed', 'Завершений'),
                               ('cancelled', 'Скасований'),
                           ],
                           default='scheduled',
                           verbose_name="Статус"
                       )
    created_at       = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at       = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        verbose_name        = "Запис"
        verbose_name_plural = "Записи"
        ordering            = ['appointment_date', 'appointment_time']
```

**Що і навіщо написано:**

`patient = models.ForeignKey(Patient, on_delete=models.CASCADE, ...)` — зовнішній ключ. У базі даних це просто числове поле `patient_id`, яке зберігає `id` пацієнта з таблиці `Patient`. Завдяки цьому Django знає, якому пацієнту належить запис.

`on_delete=models.CASCADE` — поведінка при видаленні. Якщо видалити пацієнта — всі його записи на прийом також видаляться автоматично. Це запобігає "осиротілим" записам у таблиці.

`related_name='appointments'` — назва для зворотного доступу. Якщо маємо об'єкт пацієнта, то `patient.appointments.all()` поверне всі його записи. Без `related_name` Django генерує назву автоматично, але явна назва зручніша.

`appointment_time = models.TimeField()` — зберігає лише час (`HH:MM:SS`). Дата і час зберігаються окремо, бо це зручно для фільтрації: наприклад, показати всі записи в певний день незалежно від часу.

`status = models.CharField(choices=[...], default='scheduled')` — поле з обмеженим набором значень. У базі даних зберігається технічний рядок (`'scheduled'`), а в адмінці відображається людська назва (`'Запланований'`). `default='scheduled'` — якщо статус не вказано, автоматично встановлюється значення "Запланований".

`ordering = ['appointment_date', 'appointment_time']` — сортування за двома полями: спочатку за датою, а якщо дати однакові — за часом.

---

## Типи даних — зведена таблиця

| Django-поле | Що зберігається в БД | Коли використовувати |
|---|---|---|
| `AutoField` | ціле число, автоінкремент | первинний ключ |
| `CharField(max_length=N)` | рядок до N символів | ім'я, заголовок, телефон |
| `TextField` | текст будь-якої довжини | опис, коментар, адреса |
| `EmailField` | рядок до 254 символів | email (з перевіркою формату) |
| `DateField` | дата `YYYY-MM-DD` | дата народження, дата запису |
| `TimeField` | час `HH:MM:SS` | час прийому |
| `DateTimeField` | дата + час | дата створення/оновлення |
| `ForeignKey` | ціле число (id іншої таблиці) | зв'язок між таблицями |

---

## Файл `admin.py` — повний розбір

Після створення моделей їх потрібно зареєструвати в адмін-панелі Django. Без цього кроку моделі існують у базі, але в адмінці їх не буде видно.

```python
from django.contrib import admin
from .models import Doctor, Patient, Appointment

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'specialization', 'phone', 'email', 'created_at', 'updated_at')
    search_fields = ('name', 'specialization', 'email', 'phone')
    list_filter   = ('specialization', 'created_at', 'updated_at')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'email', 'phone', 'address', 'date_of_birth', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'phone')
    list_filter   = ('date_of_birth', 'created_at', 'updated_at')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display  = ('id', 'patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'created_at', 'updated_at')
    search_fields = ('patient__name', 'doctor__name', 'description')
    list_filter   = ('status', 'appointment_date', 'doctor', 'created_at', 'updated_at')
```

**Що і навіщо написано:**

`@admin.register(Doctor)` — декоратор, який реєструє модель `Doctor` в адмінці та прив'язує до неї клас налаштувань `DoctorAdmin`. Це сучасний спосіб реєстрації — замість старого `admin.site.register(Doctor, DoctorAdmin)`.

`list_display` — кортеж з назвами полів, які відображаються як колонки у списку записів. Саме тут вказуються `created_at` і `updated_at`, щоб виконати вимогу завдання — показувати дати.

`search_fields` — поля, по яких працює рядок пошуку в адмінці. Наприклад, якщо написати ім'я — Django шукатиме його в полях `name`, `specialization` тощо.

`list_filter` — бічна панель фільтрів. Наприклад, фільтр по `status` у `AppointmentAdmin` дозволяє одним кліком показати лише "Заплановані" або лише "Скасовані" записи.

`'patient__name'` у `search_fields` — пошук через пов'язану модель. Подвійне підкреслення `__` означає "перейди у пов'язану таблицю і шукай там по полю `name`". Так можна знайти запис, написавши ім'я пацієнта.

---

## Послідовність команд та що кожна робить

### 1. Написати моделі у `models.py`

Це ручна робота — описати класи з полями. Поки що нічого в базі не змінилось, це лише Python-код.

### 2. Створити міграцію

```bash
python manage.py makemigrations
```

Django читає `models.py`, порівнює з попереднім станом і генерує файл `shop/migrations/0001_initial.py`. Це автоматично згенерований Python-файл з описом усіх змін. Його не треба редагувати вручну — він створюється командою.

### 3. Застосувати міграцію до бази даних

```bash
python manage.py migrate
```

Ця команда бере всі файли міграцій і виконує реальні SQL-запити до бази. Тільки після цієї команди таблиці `shop_doctor`, `shop_patient`, `shop_appointment` фізично з'являються у файлі `db.sqlite3`.

### 4. Написати `admin.py`

Зареєструвати моделі в адмінці з потрібними налаштуваннями — `list_display`, `search_fields`, `list_filter`.

### 5. Створити суперкористувача

```bash
python manage.py createsuperuser
```

Команда запитає логін, email і пароль. Цей користувач матиме доступ до адмін-панелі.

### 6. Запустити сервер і додати дані через адмінку

```bash
python manage.py runserver
```

Відкрити `http://127.0.0.1:8000/admin/`, увійти та вручну додати кілька лікарів, пацієнтів і записів через інтерфейс адмінки.

---

## Як таблиці пов'язані між собою

```
Patient ──────────────────────────────────────┐
  id=1, name="Іван Петренко"                  │
                                               ▼
                                         Appointment
Doctor ────────────────────────────────►   patient_id = 1
  id=3, name="Марія Коваль"                doctor_id = 3
                                           date = 2026-04-10
                                           status = 'scheduled'
```

У таблиці `shop_appointment` немає імен лікаря чи пацієнта — там зберігаються лише їхні `id`. Django сам підтягує потрібні дані з пов'язаних таблиць, коли це потрібно. Якщо лікаря видалять — запис на прийом теж зникне (`CASCADE`).
