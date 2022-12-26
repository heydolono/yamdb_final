from random import sample

from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin, )
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from reviews.models import Category, Genre, Review, Title, User
from .permissions import IsAdmin, IsAuthorOrModeratorOrReadOnly, ReadOnly
from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    PostTitleSerializer, ReviewSerializer, SignUpSerializer, TitleSerializer,
    TokenObtainSerializer, UserNotAdminSerializer, UserSerializer, )


@api_view(['POST', ])
@permission_classes([AllowAny, ])
def signup(request):
    """Контроллер для самостоятельной регистрации пользователей."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = User.objects.get_or_create(**serializer.validated_data)
    except IntegrityError:
        return Response(
            status=status.HTTP_400_BAD_REQUEST, data={'detail': (
                'Нельзя зарегистрироваться на уже '
                'существующий никнейм или почту.')})
    user.confirmation_code = ''.join(
        sample('0123456789', settings.CODE_LENGTH))
    user.save()
    send_mail('Код подтверждения', user.confirmation_code,
              settings.EMAIL_HOST_USER, (user.email, ), fail_silently=False)
    return Response(status=status.HTTP_200_OK, data=serializer.data)


@api_view(['POST', ])
@permission_classes([AllowAny, ])
def token_obtain(request):
    """Контроллер получения access токена по юзернейму и коду подтверждения."""
    serializer = TokenObtainSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data.get('username'))
    if user.confirmation_code != (
            serializer.validated_data.get('confirmation_code')):
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'detail': 'Неверно указан код подтверждения.'})
    return Response(
        status=status.HTTP_200_OK,
        data={"access": str(RefreshToken.for_user(user).access_token)})


class UserViewSet(ModelViewSet):
    """Класс контроллера для модели пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, )
    filter_backends = (SearchFilter, )
    search_fields = ('username', )
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'], detail=False,
        permission_classes=(IsAuthenticated, ),
        serializer_class=UserNotAdminSerializer)
    def me(self, request):
        """Метод эндпоинта с информацией о себе."""
        if request.method == 'GET':
            return Response(
                data=self.get_serializer(request.user).data,
                status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TitleViewSet(ModelViewSet):
    """Класс контроллера для модели произведение."""
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (IsAdmin | ReadOnly, )
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = TitleFilter
    ordering_fields = ('-year', 'rating', 'name')

    def get_serializer_class(self):
        if self.action not in ('list', 'retrieve'):
            return PostTitleSerializer
        return super(TitleViewSet, self).get_serializer_class()


class BaseSectionViewSet(
        GenericViewSet, CreateModelMixin, DestroyModelMixin, ListModelMixin):
    """
    Базовый класс контроллера для получения списка,
    создания и удаления объектов моделей категория и жанр.
    """
    permission_classes = (IsAdmin | ReadOnly, )
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class CategoryViewSet(BaseSectionViewSet):
    """Класс контроллера для модели категория."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseSectionViewSet):
    """Класс контроллера для модели жанр."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(ModelViewSet):
    """Класс контроллера для модели отзыв."""
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticated | ReadOnly, IsAuthorOrModeratorOrReadOnly, )

    def get_queryset(self):
        """Метод возвращает отзывы к этому произведению."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def get_title(self, key='title_id'):
        """Метод получения произведения по его первичному ключу."""
        return get_object_or_404(Title, id=self.kwargs.get(key))


class CommentViewSet(ModelViewSet):
    """Класс контроллера для модели комментарий."""
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticated | ReadOnly, IsAuthorOrModeratorOrReadOnly, )

    def get_queryset(self):
        """Метод возвращает комментарии к этому отзыву."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

    def get_review(self, key='review_id'):
        """Метод получения отзыва по его первичному ключу."""
        return get_object_or_404(Review, id=self.kwargs.get(key))
