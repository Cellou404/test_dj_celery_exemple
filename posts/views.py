from rest_framework import viewsets
from rest_framework.response import Response

from .models import Article
from .models import Comment
from .models import Subscriber

from .serializers import ArticleSerializer
from .serializers import CommentSerializer
from .serializers import SubcriberSerializer

from .tasks import send_top_article_notification

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "uid"

    def perform_create(self, serializer):
        # Crée l'article
        article = serializer.save(author=self.request.user)

        # Si c'est un top article, déclencher l'envoi des emails
        if article.is_top_article:
            send_top_article_notification.delay(article.uid)

        return Response({"message": "Article créé, et les emails sont envoyés si c'est un top article."})
    

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "uid"

    def perform_create(self, serializer):
        article = Article.objects.get(uid=self.kwargs['article_uid'])
        serializer.save(author=self.request.user, article=article)
        return Response(serializer.data)
    

class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubcriberSerializer
