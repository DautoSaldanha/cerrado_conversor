import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_conversor.projeto_conversor.settings')

application = get_asgi_application()