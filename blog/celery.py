from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Indiquer à Celery de prendre les paramètres Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

app = Celery('blog')

# Charger les tâches du fichier settings.py, section CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Découverte automatique des tâches dans les applications Django
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
