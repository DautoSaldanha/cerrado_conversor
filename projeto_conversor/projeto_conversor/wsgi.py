import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_conversor.projeto_conversor.settings')
application = get_wsgi_application()