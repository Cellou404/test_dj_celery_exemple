from __future__ import absolute_import, unicode_literals
# Importer l'instance Celery
from .celery import app as celery_app

# Exposer Celery comme variable pour qu'il soit accessible dans d'autres modules
__all__ = ('celery_app',)
