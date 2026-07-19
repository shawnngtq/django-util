# django-util

A Django application that provides generic utility.

- [django-util](#django-util)
  - [Installation](#installation)
  - [Utilities](#utilities)
  - [Reference](#reference)

## Installation

```bash
pip install django-util
```

## Utilities

Standalone helpers (no need to add the app to `INSTALLED_APPS`):

- `django_util.utility.init_django(django_dir, project_name=None)` - bootstrap Django
  from external scripts/notebooks.
- `django_util.utility.get_django_countries_dict()` - code↔name maps.
  Requires the optional `django-countries` package.
- `django_util.validators.django_validate_email(email, whitelist_domains=None)`
- `django_util.validators.django_validate_url(url, allowed_schemes=None)`
- `django_util.validators.django_validate_phone(phone, region=None)` - returns E.164.
  Requires the optional `django-phonenumber-field` package.

## Reference

<https://docs.djangoproject.com/en/4.2/intro/reusable-apps/>
