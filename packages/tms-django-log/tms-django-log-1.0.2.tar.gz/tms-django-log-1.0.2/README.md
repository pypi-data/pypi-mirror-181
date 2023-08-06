# Django Log Shortcut

Install the package

```bash
pip install tms_django_log
```

Add the application in the `INSTALLE_APPS`:

```python
INSTALLED_APPS = [
    ...
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'tms_django_log',
    ...
]
```

Apply migrations

```python
python manage.py migrate
```

Then use the shortcut
```python
from tms_django_log.models import add_log

add_log("Something happened", detail="More details here", level=3)
```

