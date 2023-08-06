# django-zencache

Django cache backend for ZenCached.

## Install

```
pip install django-zencache
```

## Usage

*pro/settings.py*

```
# ...

CACHES = {
    "default": {
        "BACKEND": "django_zencache.DjangoZenCache",
        "LOCATION": "127.0.0.1:6779",
        "OPTIONS": {
            "pool_size": 10,
            "username": "app01",
            "password": "spnPF3HzY975GJYC"
        }
    },
}

# ...
```

Add CACHES in `pro/settings.py`, using `django_zencache.DjangoZenCache` as the backend.

## Releases

### v0.1.0

- First release.
