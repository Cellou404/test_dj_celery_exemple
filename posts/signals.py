# blog/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article
from .tasks import send_top_article_notification


@receiver(post_save, sender=Article)
def send_email_on_top_article_creation(sender, instance, created, **kwargs):
    if created and instance.is_top_article:
        # Si un article est créé et qu'il est un top article, envoyer l'email
        send_top_article_notification.delay(instance.uid)
