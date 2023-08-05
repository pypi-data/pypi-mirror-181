# [Django Admin Berry](https://github.com/app-generator/django-admin-berry)

Modern template for **Django Admin Interface** coded on top of **Berry Dashboard**, an open-source `Boostrap 5` design from [CodedThemes](https://codedthemes.com/?ref=appseed). It is designed to deliver the best possible user experience with highly customizable feature-rich pages. `Berry` has easy and intuitive responsive design whether it is viewed on retina screens or laptops.

> Actively supported by [AppSeed](https://appseed.us/) via `Email` and `Discord`.

<br>

**Links & Resources**

- UI Kit: [Berry BS5](https://github.com/app-generator/cth-berry-bootstrap5) `v1.0.1` by CodedThemes
  - `Persistent` **Dark-Mode**
- [Django Berry Dashboard](https://github.com/app-generator/django-berry-dashboard) - `playground project`
- Sections Covered: 
  - `admin` sections, reserved for superusers
  - `All pages` managed by `Django.contrib.AUTH`
  - `Registration` page
  - `Misc pages`: colors, icons, typography, blank-page 

<br />

![Berry Bootstrap 5 - Dark-Mode ready, Open-source Template.](https://user-images.githubusercontent.com/51070104/203366808-c93b852d-d70c-4b2d-86f2-c146e5f5a05c.jpg)

<br />

## Why `Django Admin Berry`

- Modern [Bootstrap 5](https://www.admin-dashboards.com/bootstrap-5-templates/) Design
- `Responsive Interface`
- `Minimal Template` overriding
- `Easy integration`

Berry Dashboard comes with error/bug-free, well structured codebase that renders nicely in all major browsers and devices. 

<br />

## How to use it

<br />

> **Install the package** via `PIP` 

```bash
$ pip install django-admin-berry
// OR
$ pip install git+https://github.com/app-generator/django-admin-berry.git
```

<br />

> Add `admin_berry` application to the `INSTALLED_APPS` setting of your Django project `settings.py` file (note it should be before `django.contrib.admin`):

```python
    INSTALLED_APPS = (
        ...
        'admin_berry.apps.AdminBerryConfig',
        'django.contrib.admin',
    )
```

<br />

> Add `LOGIN_REDIRECT_URL` and `EMAIL_BACKEND` of your Django project `settings.py` file:

```python
    LOGIN_REDIRECT_URL = '/'
    # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

<br />

> Add `admin_berry` urls in your Django Project `urls.py` file

```python
    from django.urls import path, include

    urlpatterns = [
        ...
        path('', include('admin_berry.urls')),
    ]
```

<br />

> **Collect static** if you are in `production environment`:

```bash
$ python manage.py collectstatic
```

<br />

> **Start the app**

```bash
$ # Set up the database
$ python manage.py makemigrations
$ python manage.py migrate
$
$ # Create the superuser
$ python manage.py createsuperuser
$
$ # Start the application (development mode)
$ python manage.py runserver # default port 8000
```

Access the `admin` section in the browser: `http://127.0.0.1:8000/`

<br />

## Screenshots

@ToDo

<br />

---
**[Django Admin Berry](https://github.com/app-generator/django-admin-berry)** - Modern Admin Interface provided by **[AppSeed](https://appseed.us/)**
