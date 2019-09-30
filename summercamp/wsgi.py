"""
WSGI config for summercamp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
#from whitenoise.django import DjangoWhiteNoise ---> IMPORTERROR
# Your WhiteNoise configuration is incompatible with WhiteNoise v4.0
from whitenoise import WhiteNoise
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'summercamp.settings')

application = get_wsgi_application()
# might need whitenoise
#application = DjangoWhiteNoise(application) --> see above error
application = WhiteNoise(application)
