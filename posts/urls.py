from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .views import ArticleViewSet
from .views import CommentViewSet
from .views import SubscriberViewSet

router = DefaultRouter()
router.register(r'posts', ArticleViewSet)
router.register(r'subscribers', SubscriberViewSet)

article_router = NestedDefaultRouter(router, 'posts', lookup='article')
article_router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(article_router.urls)),
]
