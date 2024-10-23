from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Subscriber
from .models import Comment


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


@shared_task
def send_comment_notification(comment_uid):
    try:
        comment = Comment.objects.get(uid=comment_uid)
    except Comment.DoesNotExist:
        return f"Comment {comment_uid} n'existe pas."

    article = comment.article
    subject = f"Nouveau commentaire sur l'article: {article}"
    message = f"Nouveau commentaire a été ajouté sur l'article: {article}\n\n{comment.content}"
    reciepient = article.author.email
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [reciepient],
        fail_silently=False,
    )
    return f"Email envoyé à {reciepient} pour le commentaire: {comment_uid}."
