"""
WSGI config for NoInventoryProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys
import django.core.handlers.wsgi
from dj_static import Cling
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NoInventoryProject.settings")

application = get_wsgi_application()
application = Cling(get_wsgi_application())
