"""
<<<<<<< HEAD
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SmartCourt.settings")
django.setup()
application = get_default_application()
=======
ASGI config for SmartCourt project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartCourt.settings')

application = get_asgi_application()
>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4
