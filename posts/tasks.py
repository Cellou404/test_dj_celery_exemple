from celery import shared_task
from django.core.mail import send_mail
from .models import Subscriber


@shared_task
def send_top_article_notification(article_uid):
    from .models import Article

    try:
        article = Article.objects.get(uid=article_uid)
    except Article.DoesNotExist:
        return f"Article {article_uid} n'existe pas."

    # Récupérer tous les abonnés
    subscribers = Subscriber.objects.all()
    recipient_list = [subscriber.email for subscriber in subscribers]

    if recipient_list:
        send_mail(
            f"Nouveau top article : {article.title}",
            f"Découvrez notre nouvel article : {article.title}\n\n{article.content}",
            'cellou649@gmail.com',
            recipient_list,
            fail_silently=False,
        )
        return f"Emails envoyés à {len(recipient_list)} abonnés."
    else:
        return "Aucun abonné trouvé pour cet article."
