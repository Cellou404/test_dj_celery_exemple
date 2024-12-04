from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .models import Article
from .models import Comment
from .models import Subscriber

from .serializers import ArticleSerializer
from .serializers import CommentSerializer
from .serializers import SubcriberSerializer

from .tasks import send_top_article_notification
from .tasks import send_comment_notification

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "uid"

    def perform_create(self, serializer):
        article = serializer.save(author=self.request.user)


        if article.is_top_article:
            send_top_article_notification.apply_async(kwargs={'article_uid': article.uid})

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "uid"

    def perform_create(self, serializer):
        article = Article.objects.get(uid=self.kwargs['article_uid'])
        comment = serializer.save(author=self.request.user, article=article)
        send_comment_notification.apply_async(kwargs={'comment_uid': comment.uid})
        return Response(serializer.data)


class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubcriberSerializer
