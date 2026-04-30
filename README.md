# Лабораторна робота 5 — Документація змін проєкту `crunch`

> **Проєкт:** Django-застосунок стоматологічної клініки «Посмішка»  
> **Застосунок:** `shop` (всередині проєкту `crunch`)  
> **База даних:** SQLite (`db.sqlite3`)  
> **Фреймворк:** Django 5.2+ / Python 3.14

---

## Загальна картина

До початку Лаб 5 у проєкті вже існували:
- Django-проєкт `crunch` зі стандартними налаштуваннями (`settings.py`, `urls.py`, `wsgi.py`, `asgi.py`)
- Застосунок `shop` з трьома моделями: `Doctor`, `Patient`, `Appointment`
- Початкова міграція `0001_initial.py` (створена 01.04.2026)
- Базові view-функції та URL-маршрути для сторінок: `home`, `about`, `products`, `contact`

У Лаб 5 було зроблено **5 кроків**, які покрили увесь стек: від моделі БД до фінального HTML-шаблону.

---

## Крок 1 — Додавання моделі `Service` та зв'язку з `Appointment`

**Файли змінено:** `shop/models.py`, `shop/migrations/0002_service_appointment_service.py`

### Що зроблено

У `models.py` додано новий клас `Service`:

```python
class Service(models.Model):
    id          = models.AutoField(primary_key=True, verbose_name="ID")
    name        = models.CharField(max_length=255, verbose_name="Назва")
    description = models.TextField(verbose_name="Опис")
    price       = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    duration    = models.PositiveIntegerField(
                      verbose_name="Тривалість (хв)",
                      help_text="Тривалість послуги в хвилинах"
                  )
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at  = models.DateTimeField(auto_now=True,     verbose_name="Дата оновлення")

    class Meta:
        verbose_name        = "Послуга"
        verbose_name_plural = "Послуги"
        ordering            = ['name']

    def __str__(self):
        return self.name
```

**Поля моделі:**

| Поле | Тип | Призначення |
|---|---|---|
| `id` | `AutoField` | Первинний ключ |
| `name` | `CharField(255)` | Назва послуги |
| `description` | `TextField` | Детальний опис |
| `price` | `DecimalField(10, 2)` | Ціна в гривнях |
| `duration` | `PositiveIntegerField` | Тривалість у хвилинах |
| `created_at` | `DateTimeField(auto_now_add)` | Дата/час створення запису |
| `updated_at` | `DateTimeField(auto_now)` | Дата/час останнього оновлення |

Також у модель `Appointment` додано зовнішній ключ на `Service`:

```python
service = models.ForeignKey(
    Service,
    on_delete=models.CASCADE,
    related_name='appointments',
    verbose_name="Послуга",
    default=1
)
```

Це означає, що кожен запис до лікаря тепер обов'язково пов'язаний з конкретною послугою. `default=1` дозволяє безпечно застосувати міграцію до вже існуючих записів у БД без помилки `NOT NULL`.

Рядок `__str__` у `Appointment` також оновлено, щоб включати назву послуги:

```python
def __str__(self):
    return f"{self.patient.name} - {self.doctor.name} - {self.service.name}"
```

### Команди, які виконувались

```bash
python manage.py makemigrations
python manage.py migrate
```

Результат — файл міграції `0002_service_appointment_service.py`, який:
1. Створює таблицю `shop_service`
2. Додає стовпець `service_id` до таблиці `shop_appointment` з `DEFAULT 1`

---

## Крок 2 — Реєстрація моделей у Django Admin

**Файл змінено:** `shop/admin.py`

### Що зроблено

Зареєстровано всі чотири моделі через декоратор `@admin.register` з налаштованими класами `ModelAdmin`:

```python
from django.contrib import admin
from .models import Doctor, Patient, Service, Appointment

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

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'description', 'price', 'duration', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter   = ('price', 'duration', 'created_at', 'updated_at')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display  = ('id', 'patient', 'doctor', 'service', 'appointment_date', 'appointment_time', 'status', 'created_at', 'updated_at')
    search_fields = ('patient__name', 'doctor__name', 'service__name', 'description')
    list_filter   = ('status', 'appointment_date', 'doctor', 'service', 'created_at', 'updated_at')
```

### Що дає кожен параметр

- **`list_display`** — колонки, які відображаються у списку об'єктів на сторінці адмінки
- **`search_fields`** — поля, по яких працює рядок пошуку у верхній частині списку
- **`list_filter`** — бічна панель фільтрів праворуч (фільтрація по статусу, даті, лікарю тощо)

Для `AppointmentAdmin` у `search_fields` використано `__`-нотацію для пошуку через зовнішній ключ (`patient__name`, `doctor__name`, `service__name`).

---

## Крок 3 — Базовий шаблон `base.html` та файл стилів `style.css`

**Файли створено:** `shop/templates/shop/base.html`, `shop/static/shop/css/style.css`

### Структура `base.html`

Базовий шаблон — єдина точка розширення для всіх сторінок. Він підключає Bootstrap та власний CSS, містить навігацію та футер:

```html
{% load static %}
<!-- Bootstrap 5.3.0 CDN -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<!-- Власний CSS -->
<link rel="stylesheet" href="{% static 'shop/css/style.css' %}">
```

**Навігація (`<nav>`)** — Bootstrap Navbar з посиланнями на 4 сторінки (`home`, `about`, `products`, `contact`), використовується `{% url 'shop:...' %}` з namespace `shop`.

**Блок контенту:**
```html
<div class="content">
    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>
</div>
```

**Футер** — три колонки: назва клініки з описом, контактні дані, швидкі посилання.

**`<body>`** використовує flexbox (`display: flex; flex-direction: column; min-height: 100vh`) — це класичний прийом «липкого футера», щоб футер завжди залишався внизу.

### Файл стилів `style.css`

Підключається через `{% load static %}` і `{% static %}`. Визначає наступні секції:

| Клас / секція | Що стилізує |
|---|---|
| `.hero-section` | Повноширокий банер з градієнтним фоном `#667eea → #764ba2` |
| `.btn-primary-custom` | Зелена кнопка заклику до дії (CTA) |
| `.about-section` | Секція «Про нас» зі світло-сірим фоном `#f8f9fa` |
| `.gallery-section` | Секція галереї (стилі залишено, сама секція видалена з `home.html`) |
| `.services-section` | Секція карток послуг зі світлим фоном |
| `.service-card` | Картка послуги: `border-radius`, `box-shadow`, `transition: transform 0.3s` — ефект підняття при наведенні |
| `.cta-section` | Секція заклику внизу сторінки — той самий градієнт, що й у hero |
| `.navbar-brand` | Назва клініки у навбарі — синій колір `#007bff` жирним шрифтом |
| `.footer` | Сірий фон, відступ зверху |
| `body`, `.content` | Flexbox-розкладка для липкого футера |

---

## Крок 4 — Головна сторінка `home.html`

**Файл змінено:** `shop/templates/shop/home.html`

### Що зроблено

Шаблон `home.html` повністю перероблено. Він розширює `base.html` (`{% extends 'shop/base.html' %}`) і містить 4 секції:

**1. Hero-секція**
```html
<section class="hero-section">
    <h1>Стоматологічна клініка «Посмішка»</h1>
    <p>Опис клініки...</p>
    <a href="{% url 'shop:products' %}" class="btn btn-primary btn-primary-custom">Записатися на прийом</a>
</section>
```
Великий банер з градієнтним фоном, заголовком та кнопкою, яка веде на сторінку послуг.

**2. Секція «Про нас»**
Два стовпці Bootstrap (по `col-md-6`) з текстом про клініку та команду лікарів.

**3. Секція «Наші послуги»** (статична)
Сітка `row` з 6 картками `col-md-4` — по 3 на рядок. Кожна картка використовує клас `.service-card` та містить назву й опис послуги. Дані в цій секції **жорстко прописані в HTML** (не з БД — це відрізняє від кроку 5).

**4. CTA-секція**
```html
<section class="cta-section">
    <h2>Готові до ідеальної посмішки?</h2>
    <a href="{% url 'shop:contact' %}" class="btn btn-light btn-lg">Зв'язатися з нами</a>
</section>
```

> **Примітка:** Секцію галереї з фотографіями (`.gallery-section`), яка планувалась раніше, було **видалено** з фінальної версії `home.html` (стилі в CSS збереглися, але сама розмітка прибрана).

---

## Крок 5 — Сторінка послуг з даними з БД

**Файли змінено:** `shop/views.py`, `shop/templates/shop/products.html`  
**Файл створено:** `shop/fixtures/services.json`

### Оновлення `views.py`

До цього кроку `products` view повертав порожній контекст. Тепер він робить запит до БД:

```python
from django.shortcuts import render
from .models import Service

def products(request):
    services = Service.objects.all()   # <-- запит до таблиці shop_service
    context = {
        'title': 'Наші послуги',
        'services': services           # <-- QuerySet передається в шаблон
    }
    return render(request, 'shop/products.html', context)
```

`Service.objects.all()` повертає `QuerySet` з усіма записами, відсортованими за `name` (за `Meta.ordering`).

### Оновлення `products.html`

Шаблон ітерується по `QuerySet` через `{% for service in services %}`:

```html
{% for service in services %}
<div class="col-md-4 mb-4">
    <div class="service-card">
        <h3>{{ service.name }}</h3>
        <p>{{ service.description }}</p>
        <p><strong>Ціна:</strong> {{ service.price }} грн</p>
        <p><strong>Тривалість:</strong> {{ service.duration }} хв</p>
        <a href="{% url 'shop:contact' %}" class="btn btn-primary">Записатися</a>
    </div>
</div>
{% empty %}
<p class="text-center">Послуги ще не додані.</p>
{% endfor %}
```

Тег `{% empty %}` відображається, якщо QuerySet порожній — зручна заглушка на випадок відсутності даних.

### Фікстури `fixtures/services.json`

Щоб одразу заповнити БД тестовими даними, створено файл фікстур з 6 послугами:

| pk | Назва | Ціна (грн) | Тривалість (хв) |
|---|---|---|---|
| 1 | Лікування карієсу | 500.00 | 60 |
| 2 | Протезування зубів | 2000.00 | 120 |
| 3 | Чищення зубів | 300.00 | 45 |
| 4 | Виправлення прикусу | 1500.00 | 30 |
| 5 | Імплантація зубів | 3000.00 | 90 |
| 6 | Дитяча стоматологія | 250.00 | 30 |

Завантаження фікстур у БД:

```bash
python manage.py loaddata services
```

---

## Підсумкова схема змін

```
Лаб 5
│
├── Крок 1 ── models.py
│              ├── + клас Service (name, description, price, duration)
│              ├── + ForeignKey service у Appointment (default=1)
│              ├── + оновлено __str__ Appointment
│              └── migrations/0002_service_appointment_service.py
│
├── Крок 2 ── admin.py
│              ├── @admin.register(Doctor)   → DoctorAdmin
│              ├── @admin.register(Patient)  → PatientAdmin
│              ├── @admin.register(Service)  → ServiceAdmin
│              └── @admin.register(Appointment) → AppointmentAdmin
│
├── Крок 3 ── templates/shop/base.html
│              ├── Bootstrap 5.3.0 CDN
│              ├── Navbar з 4 посиланнями
│              ├── {% block content %}
│              └── Footer (3 колонки)
│             static/shop/css/style.css
│              └── hero, about, service-card, cta, navbar, footer, sticky-footer
│
├── Крок 4 ── templates/shop/home.html
│              ├── Hero-секція (градієнт + CTA кнопка)
│              ├── About-секція (2 колонки)
│              ├── Services-секція (6 статичних карток)
│              ├── CTA-секція
│              └── видалено gallery-секцію
│
└── Крок 5 ── views.py
│              └── products() → Service.objects.all() → context['services']
│             templates/shop/products.html
│              └── {% for service in services %} → name, description, price, duration
│             fixtures/services.json
│              └── 6 тестових послуг для loaddata
```

---

## Загальні команди для запуску проєкту

```bash
# Застосувати міграції
python manage.py migrate

# Завантажити тестові дані
python manage.py loaddata services

# Запустити сервер розробки
python manage.py runserver

# Створити суперкористувача для адмінки
python manage.py createsuperuser
```

Адмінка доступна за адресою: `http://127.0.0.1:8000/admin/`  
Сторінка послуг: `http://127.0.0.1:8000/products/`
# Лабораторна робота № 6 — Зміни та порядок виконання

> **Проєкт:** Django-додаток стоматологічної клініки `crunch`  
> **Аплікація:** `shop`  
> **База даних:** SQLite (`db.sqlite3`)

---

## Крок 1 — Додано поле `image` до моделі `Service`

**Файл:** `shop/models.py`

До вже існуючого класу `Service` додано нове поле прямо в тіло класу:

```python
image = models.ImageField(blank=True, null=True,
                          upload_to='services/',
                          verbose_name='Фото')
```

**Що це означає і чому саме так:**

- `ImageField` — спеціальний тип поля Django для зберігання зображень. Технічно це розширення `FileField`, яке додатково перевіряє, що файл є дійсним зображенням. Для роботи потребує встановленої бібліотеки `Pillow`.
- `blank=True` — поле не є обов'язковим на рівні валідації форм (можна зберегти послугу без фото).
- `null=True` — дозволяє зберігати `NULL` у базі даних, якщо фото не завантажено.
- `upload_to='services/'` — Django автоматично зберігає завантажені файли у папку `MEDIA_ROOT/services/`. У проєкті вже була створена порожня директорія `media/services/`.

Після збереження файлу стан моделі `Service` змінився — вона описує нову колонку `image`, якої ще немає у реальній таблиці БД.

---

## Крок 2 — Створення міграції для поля `image`

Щоб зміна в моделі відобразилася в реальній базі даних, потрібно створити та застосувати міграцію.

**Команда у терміналі:**
```bash
python manage.py makemigrations
```

Django порівняв поточний стан моделей з останньою відомою міграцією (`0002`) і автоматично згенерував новий файл:

**Файл:** `shop/migrations/0003_service_image.py`

```python
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_service_appointment_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='image',
            field=models.ImageField(blank=True, null=True,
                                    upload_to='services/', verbose_name='Фото'),
        ),
    ]
```

- `dependencies` — вказує, що ця міграція виконується після `0002`
- `AddField` — Django виконає `ALTER TABLE shop_service ADD COLUMN image` на рівні SQL

**Команда для застосування:**
```bash
python manage.py migrate
```

Після цього в таблиці `shop_service` у файлі `db.sqlite3` з'явилася нова колонка `image`.

---

## Крок 3 — Data migration: початкові дані (6 послуг)

Щоб у базі з'явились тестові дані без ручного введення через адмінку, використано **data migration** — міграція, яка виконує Python-код із вставкою даних.

**Команда для створення порожньої міграції:**
```bash
python manage.py makemigrations shop --empty --name auto_20260417_1926
```

**Файл:** `shop/migrations/0004_auto_20260417_1926.py`

У файл вручну написано функцію-наповнювач:

```python
from django.db import migrations

def create_initial_services(apps, schema_editor):
    Service = apps.get_model('shop', 'Service')
    if Service.objects.exists():
        return  # якщо записи вже є — нічого не робити (захист від повторного запуску)

    services_data = [
        {'name': 'Лікування карієсу',   'description': '...', 'price': 500.00,  'duration': 60},
        {'name': 'Протезування зубів',  'description': '...', 'price': 2000.00, 'duration': 120},
        {'name': 'Чищення зубів',       'description': '...', 'price': 300.00,  'duration': 45},
        {'name': 'Виправлення прикусу', 'description': '...', 'price': 1500.00, 'duration': 30},
        {'name': 'Імплантація зубів',   'description': '...', 'price': 3000.00, 'duration': 90},
        {'name': 'Відбілювання зубів',  'description': '...', 'price': 400.00,  'duration': 60},
    ]

    for data in services_data:
        Service.objects.create(**data)

class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_service_image'),
    ]

    operations = [
        migrations.RunPython(create_initial_services),
    ]
```

**Чому data migration, а не fixtures?**

Fixtures — це JSON/YAML файли з даними, які потрібно вручну запускати командою `loaddata`. Data migration запускається автоматично разом із `migrate`, тому дані вставляються самі при першому розгортанні проєкту.

**Важливий момент:** всередині data migration модель отримується не через прямий імпорт (`from .models import Service`), а через `apps.get_model('shop', 'Service')`. Це гарантує, що Django використовує саме ту версію моделі, яка відповідає цій міграції, а не поточну.

**Команда для застосування:**
```bash
python manage.py migrate
```

Після цього в таблиці `shop_service` з'явилось 6 записів.

---

## Крок 4 — Оновлення `ServiceAdmin` в адмінці

**Файл:** `shop/admin.py`

До поля `list_display` класу `ServiceAdmin` додано `'image'`:

```python
# Було:
list_display = ('id', 'name', 'description', 'price', 'duration', 'created_at', 'updated_at')

# Стало:
list_display = ('id', 'name', 'description', 'price', 'duration', 'image', 'created_at', 'updated_at')
```

Тепер у списку послуг в адмін-панелі `/admin/shop/service/` відображається колонка `image`, де видно шлях до файлу зображення або порожнє значення, якщо фото не завантажено.

---

## Крок 5 — Новий view `service_detail`

**Файл:** `shop/views.py`

Додано імпорт `get_object_or_404` і написано новий view:

```python
# Додано до існуючого імпорту:
from django.shortcuts import render, get_object_or_404

# Новий view:
def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    context = {
        'title': service.name,
        'service': service
    }
    return render(request, 'shop/service_detail.html', context)
```

**Як це працює:**

- View приймає параметр `service_id` з URL.
- `get_object_or_404(Service, id=service_id)` — намагається знайти об'єкт `Service` із заданим `id`. Якщо такого немає — Django автоматично повертає відповідь HTTP 404. Це коротший спосіб замість ручного `try/except Service.DoesNotExist`.
- У контекст передається весь об'єкт `service` (з усіма полями, включно з `image`).
- Django рендерить шаблон `shop/service_detail.html` із цим контекстом.

---

## Крок 6 — Новий URL для детальної сторінки

**Файл:** `shop/urls.py`

До списку `urlpatterns` додано новий маршрут:

```python
# Додано:
path('service/<int:service_id>/', views.service_detail, name='service_detail'),
```

**Пояснення:**

- `service/<int:service_id>/` — URL-шаблон з конвертером `<int:...>`: очікує ціле число, передає його як аргумент `service_id` у view.
- `name='service_detail'` — іменований URL. Завдяки цьому в шаблонах можна писати `{% url 'shop:service_detail' service.id %}` замість хардкоду `/service/1/`.

Повний список маршрутів після зміни:

```
''                           → home
'about/'                     → about
'products/'                  → products
'service/<int:service_id>/'  → service_detail   ← новий
'contact/'                   → contact
```

---

## Крок 7 — Оновлення шаблону `products.html`

**Файл:** `shop/templates/shop/products.html`

Внесено дві зміни всередині циклу `{% for service in services %}`:

**Зміна 1 — додано відображення фото:**

```html
{% if service.image %}
<img src="{{ service.image.url }}" alt="{{ service.name }}" class="img-fluid mb-3">
{% endif %}
```

Перевірка `{% if service.image %}` потрібна, щоб не виводити зламаний тег `<img>` для послуг без фото. `img-fluid` — Bootstrap-клас, що робить зображення адаптивним (ширина 100% від батьківського елемента).

**Зміна 2 — замінено кнопку "Записатися" на "Деталі":**

```html
<!-- Було: -->
<a href="..." class="btn btn-primary">Записатися</a>

<!-- Стало: -->
<a href="{% url 'shop:service_detail' service.id %}" class="btn btn-secondary me-2">Деталі</a>
```

Кнопку "Записатися" видалено, оскільки функціонал запису ще не реалізований. Замість неї — посилання на детальну сторінку конкретної послуги. `service.id` підставляється у `<int:service_id>` маршруту.

---

## Крок 8 — Новий шаблон `service_detail.html`

**Файл:** `shop/templates/shop/service_detail.html` *(новий файл)*

Створено новий HTML-шаблон для детальної сторінки послуги:

```html
{% extends 'shop/base.html' %}
{% load static %}

{% block title %}{{ service.name }}{% endblock %}

{% block content %}
<div class="container">
    <div class="row">

        <!-- Ліва колонка: зображення -->
        <div class="col-md-6">
            {% if service.image %}
            <img src="{{ service.image.url }}" alt="{{ service.name }}" class="img-fluid">
            {% else %}
            <img src="{% static 'shop/images/no-image.png' %}" alt="No image" class="img-fluid">
            {% endif %}
        </div>

        <!-- Права колонка: інформація про послугу -->
        <div class="col-md-6">
            <h1>{{ service.name }}</h1>
            <p>{{ service.description }}</p>
            <p><strong>Ціна:</strong> {{ service.price }} грн</p>
            <p><strong>Тривалість:</strong> {{ service.duration }} хв</p>
            <button class="btn btn-primary" disabled>Записатися</button>
        </div>

    </div>

    <!-- Кнопка назад -->
    <div class="mt-4">
        <a href="{% url 'shop:products' %}" class="btn btn-outline-primary">
            Повернутися до послуг
        </a>
    </div>
</div>
{% endblock %}
```

**Деталі реалізації:**

- `{% extends 'shop/base.html' %}` — шаблон успадковує навігацію, футер і Bootstrap від базового шаблону.
- Двоколонковий layout Bootstrap: `col-md-6` зліва для фото, `col-md-6` справа для тексту. На мобільних обидві колонки автоматично стають повноширинними.
- Для фото — подвійна логіка: якщо `service.image` є, виводить реальне фото через `service.image.url`; якщо немає — заглушка `no-image.png` зі статичних файлів.
- Кнопка "Записатися" навмисно має атрибут `disabled` — функціонал форми запису ще не реалізований, але кнопка вже є у макеті.
- Кнопка "Повернутися до послуг" веде через іменований URL `shop:products`.

---

## Повний порядок виконаних команд

```bash
# 1. Після додавання поля image у models.py — створити міграцію
python manage.py makemigrations

# 2. Застосувати міграцію 0003 (додає колонку image у таблицю)
python manage.py migrate

# 3. Створити порожню міграцію для початкових даних
python manage.py makemigrations shop --empty --name auto_20260417_1926

# 4. Написати функцію create_initial_services у файлі 0004_... вручну,
#    після чого застосувати міграцію (вставляє 6 послуг у таблицю)
python manage.py migrate

# 5. Запустити сервер і перевірити результат
python manage.py runserver
```

---

## Що перевіряли після запуску

| URL | Що перевіряли |
|-----|---------------|
| `/products/` | Список послуг з картками, фото (якщо є), кнопка "Деталі" |
| `/service/1/` | Детальна сторінка "Лікування карієсу" |
| `/service/3/` | Детальна сторінка "Чищення зубів" |
| `/service/999/` | Має повернути HTTP 404 |
| `/admin/shop/service/` | Список послуг з колонкою `image` в адмінці |

---

## Крок 9 — Фільтрація по категоріям

Після реалізації базового функціоналу послуг та їх детальних сторінок, було додано додатковий функціонал для фільтрації лікарів за рейтингом та вибору лікаря на сторінці послуги. Це дозволяє користувачам вибирати лікаря залежно від його рейтингу та процедур, які він проводить.

### Що додано

#### 1. Оновлення моделі `Doctor`

До моделі `Doctor` додано два нових поля:

- **`rating`** — `DecimalField(max_digits=3, decimal_places=1, default=0.0)`: рейтинг лікаря від 0.0 до 5.0
- **`procedures`** — `ManyToManyField(Service)`: зв'язок з послугами, які проводить лікар

```python
class Doctor(models.Model):
    # ... існуючі поля ...
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, verbose_name="Рейтинг")
    procedures = models.ManyToManyField('Service', blank=True, related_name='doctors', verbose_name="Процедури")
    # ... існуючі поля ...
```

Створено міграцію `0005_doctor_procedures_doctor_rating.py` та застосовано її до бази даних.

#### 2. Оновлення view-функцій

- **Оновлено `home`**: додано показ топ 3 лікаря на головній сторінці замість статичного блоку послуг
- **Оновлено `service_detail`**: додано передачу списку лікарів, які проводять цю послугу (`doctors = Doctor.objects.filter(procedures=service)`)
- **Додано нову view `doctors`**: відображає список лікарів з фільтрацією за рейтингом через GET-параметр `rating`. Фільтрація працює в діапазоні від цілого числа до наступного (наприклад, `rating=2` показує лікарів з рейтингом 2.0–2.999)

```python
def doctors(request):
    rating_filter = request.GET.get('rating')
    doctors = Doctor.objects.all()
    if rating_filter:
        try:
            rating = int(float(rating_filter))
            doctors = doctors.filter(rating__gte=rating, rating__lt=rating + 1)
        except ValueError:
            pass
    # ... решта коду ...
```

#### 3. Оновлення URL-маршрутів

Додано новий маршрут для сторінки лікарів:

```python
path('doctors/', views.doctors, name='doctors'),
```

#### 4. Оновлення Django Admin

У `DoctorAdmin` додано `rating` до `list_display` та `list_filter` для відображення та фільтрації за рейтингом у адмінці.

#### 5. Оновлення навігації (`base.html`)

Додано dropdown-меню "Лікарів" у навігації з посиланнями для фільтрації за рейтингом:

- Всі лікарі
- Рейтинг 5
- Рейтинг 4
- Рейтинг 3
- Рейтинг 2
- Рейтинг 1

Кожне посилання веде на `/doctors/?rating=X`, де X — ціле число рейтингу.

#### 6. Оновлення шаблону `service_detail.html`

На сторінці детальної послуги додано:

- Випадаючий список (select) для вибору лікаря, якщо є лікарі, які проводять цю послугу
- Кнопка "Записатися" залишається неактивною, поки не обрано лікаря (JavaScript)
- Якщо лікарів немає, показується повідомлення

```html
{% if doctors %}
<div class="mt-4">
  <label for="doctorSelect" class="form-label"><strong>Оберіть лікаря:</strong></label>
  <select id="doctorSelect" class="form-select">
    <option value="">-- Виберіть лікаря --</option>
    {% for doctor in doctors %}
    <option value="{{ doctor.id }}">{{ doctor.name }} ({{ doctor.rating }})</option>
    {% endfor %}
  </select>
</div>
<button id="bookButton" class="btn btn-primary mt-4" disabled>Записатися</button>
{% else %}
<div class="alert alert-warning mt-4">
  На цю послугу ще не призначено лікарів.
</div>
<button class="btn btn-primary mt-4" disabled>Записатися</button>
{% endif %}
```

JavaScript активує кнопку при виборі лікаря:

```javascript
const doctorSelect = document.getElementById('doctorSelect');
const bookButton = document.getElementById('bookButton');
if (doctorSelect && bookButton) {
  doctorSelect.addEventListener('change', function () {
    bookButton.disabled = !this.value;
  });
}
```

#### 7. Створення шаблону `doctors.html`

Новий шаблон для відображення списку лікарів з:

- Ім'ям, спеціалізацією, рейтингом
- Текстовим коефіцієнтом ціни залежно від рейтингу:
  - Рейтинг 3.0: коефіцієнт 1.0 (ціна така сама)
  - Рейтинг > 3.0: коефіцієнт 1.1 (ціна зростає)
  - Рейтинг < 3.0: коефіцієнт 0.9 (ціна зменшується)
- Описом, контактними даними, списком процедур

#### 8. Оновлення стилів (`style.css`)

Додано стилі для `.doctor-card` аналогічно `.service-card`: `border-radius`, `box-shadow`, `transition` для ефекту підняття при наведенні.

#### 9. Створення fixture `doctors.json`

Додано 11 лікарів з різними рейтингами (від 1.9 до 5.0) та прив'язаними процедурами. Завантажено через `python manage.py loaddata shop/fixtures/doctors.json`.

### Команди, які виконувались

```bash
# Створення міграції для нових полів у Doctor
python manage.py makemigrations
python manage.py migrate

# Завантаження fixture з лікарями
python manage.py loaddata shop/fixtures/doctors.json

# Перевірка
python manage.py check
python manage.py runserver
```

### Що перевіряли після запуску

| URL | Що перевіряли |
|-----|---------------|
| `/doctors/` | Список всіх лікарів з коефіцієнтами ціни |
| `/doctors/?rating=5` | Тільки лікарі з рейтингом 5.0–5.999 |
| `/doctors/?rating=2` | Тільки лікарі з рейтингом 2.0–2.999 |
| `/service/1/` | Вибір лікаря для "Лікування карієсу" (якщо є лікарі, які його проводять) |
| `/admin/shop/doctor/` | Список лікарів з колонкою `rating` та фільтром за рейтингом |

Цей функціонал дозволяє користувачам фільтрувати лікарів за рейтингом через навігацію та вибирати конкретного лікаря на сторінці послуги перед записом.
