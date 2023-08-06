import django

version = "2.6.0"

if django.VERSION < (3, 2):
    default_app_config = "admin_ui.apps.AdminUIConfig"
