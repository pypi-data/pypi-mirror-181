# Pursuit Library - Django

This package provides utility functions and classes for Django (and Select2).

It also contains static files for:

- [Jquery](https://jquery.com/) 3.6.0
- [Select2](https://github.com/select2/select2) 4.1.0-rc.0
- [Bootstrap](https://getbootstrap.com/) 5.1.3 (JS only, a customized CSS must be provided)
- [FontAwesome](https://fontawesome.com/) 5.15.4

## Configuration

The following values should be added to the Django configuration:

```python
VERSION = "PROJECT_VERSION"
DEV_STAGE = "PROJECT_DEV_STAGE"
DISPLAY_VERSION = VERSION if DEV_STAGE is None else VERSION + " " + DEV_STAGE

DOMAIN = get_env('PROJECTNAME_DOMAIN')
USE_HTTPS = get_env('PROJECTNAME_USE_HTTPS').lower() == 'true'
BASE_URL = ("https://" if USE_HTTPS else "http://") + DOMAIN
```

## Error handling

To enable error handling, add he following lines to your main `urls.py` file:

```python
# Error handling

handler400 = "pursuitlib_django.errors.error_400"
handler403 = "pursuitlib_django.errors.error_403"
handler404 = "pursuitlib_django.errors.error_404"
```
