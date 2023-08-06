from __future__ import unicode_literals

from django.apps import AppConfig

__all__ = ["AdminUIConfig"]


class AdminUIConfig(AppConfig):
    name = "admin_ui"
    label = "admin_ui"
    verbose_name = "AdminUI"
