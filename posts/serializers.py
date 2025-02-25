from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Article
from .models import Comment
from .models import Subscriber
from .tasks import send_top_article_notification


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')
        extra_kwargs = {
            'password': {'write_only': True},
        }


class BaseCommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('uid', 'author', 'content')


class ArticleSerializer(serializers.ModelSerializer):
    author = AuthSerializer(read_only=True)
    comments = serializers.SerializerMethodField(method_name='get_comments')

    class Meta:
        model = Article
        fields = (
            'uid', 'title', 'content',
            'author', 'is_top_article', 'comments'
        )
        extra_kwargs = {
            'uid': {'read_only': True},
            'author': {'read_only': True},
            'comments': {'read_only': True},
        }

    def get_comments(self, obj):
        comments = Comment.objects.filter(article=obj)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    def create(self, validated_data):
        author = self.context['request'].user
        article = Article.objects.create(
            author=author,
            **validated_data
        )
        send_top_article_notification.apply_async(args={
            "article_uid": article.uid,
        })


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'uid', 'author', 'article', 'content',
            'name', 'email', 'created_at', 'updated_at',
        )
        extra_kwargs = {
            'uid': {'read_only': True},
            'author': {'read_only': True},
            'article': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }


class SubcriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ('email',)
