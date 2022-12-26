from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet,
    signup, TitleViewSet, token_obtain, UserViewSet)

router_v1 = DefaultRouter()

router_v1.register(r'users', UserViewSet, basename='user')
router_v1.register(r'titles', TitleViewSet, basename='title')
router_v1.register(r'categories', CategoryViewSet, basename='category')
router_v1.register(r'genres', GenreViewSet, basename='genre')
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review')
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment')

registration_urlpatterns = [
    path('signup/', signup, name='signup'),
    path('token/', token_obtain, name='token_obtain'),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(registration_urlpatterns)),
]
