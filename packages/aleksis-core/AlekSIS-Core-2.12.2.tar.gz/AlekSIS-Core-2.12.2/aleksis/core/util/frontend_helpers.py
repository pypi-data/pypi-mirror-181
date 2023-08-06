import os

from django.conf import settings

from .core_helpers import get_app_module, get_app_packages


def get_apps_with_assets():
    """Get a dictionary of apps that ship frontend assets."""
    assets = {}
    for app in get_app_packages():
        mod = get_app_module(app, "apps")
        path = os.path.join(os.path.dirname(mod.__file__), "assets")
        if os.path.isdir(path):
            package = ".".join(app.split(".")[:-2])
            assets[package] = path
    return assets


def get_language_cookie(code: str) -> str:
    """Build a cookie string to set a new language."""
    cookie_parts = [f"{settings.LANGUAGE_COOKIE_NAME}={code}"]
    args = dict(
        max_age=settings.LANGUAGE_COOKIE_AGE,
        path=settings.LANGUAGE_COOKIE_PATH,
        domain=settings.LANGUAGE_COOKIE_DOMAIN,
        secure=settings.LANGUAGE_COOKIE_SECURE,
        httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
        samesite=settings.LANGUAGE_COOKIE_SAMESITE,
    )
    cookie_parts += [f"{k.replace('_', '-')}={v}" for k, v in args.items() if v]
    return "; ".join(cookie_parts)
