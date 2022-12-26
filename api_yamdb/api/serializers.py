from django.conf import settings
from rest_framework import serializers

from reviews.models import (
    Category, Comment, Genre, Review, Title, User)
from reviews.validators import validate_username, validate_year


class UserSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для модели пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role', )
        lookup_field = 'username'

    def validate_username(self, value):
        return validate_username(value)


class SignUpSerializer(serializers.Serializer):
    """
    Класс-сериализатор для модели пользователя, используемый для
    самостоятельной регистрации пользователей.
    """
    username = serializers.CharField(
        required=True, max_length=settings.USERNAME_LENGTH,
        validators=[validate_username])
    email = serializers.EmailField(
        required=True, max_length=settings.EMAIL_LENGTH)


class TokenObtainSerializer(serializers.Serializer):
    """Класс-сериализатор для получения токена."""
    username = serializers.CharField(
        required=True, max_length=settings.USERNAME_LENGTH,
        validators=[validate_username])
    confirmation_code = serializers.CharField(
        required=True, max_length=settings.CODE_LENGTH)


class UserNotAdminSerializer(UserSerializer):
    """
    Класс-сериализатор для модели пользователя,
    используемый для пользователей без прав администратора.
    """

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role', )


class CategorySerializer(serializers.ModelSerializer):
    """Класс-сериализатор для модели категория."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для модели жанр."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для модели произведение на чтение."""
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')


class PostTitleSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для модели произведение на создание и изменение."""
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), required=True,
        many=True, slug_field='slug')
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), required=True, slug_field='slug')

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        return validate_year(value)


class BasePostSerializer(serializers.ModelSerializer):
    """Базовый класс-сериализатор для моделей отзыв и комментарий."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault())


class ReviewSerializer(BasePostSerializer):
    """Класс-сериализатор модели отзыв."""
    title = serializers.HiddenField(default=None)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title', )

    def validate(self, data):
        if self.context.get('request').method == 'POST' and (
            Review.objects.filter(
                author=self.context.get('request').user,
                title__id=self.context.get('view').kwargs.get('title_id')
            ).exists()
        ):
            raise serializers.ValidationError(
                'Вы можете оставить только один отзыв на это произведение.')
        return data


class CommentSerializer(BasePostSerializer):
    """Класс-сериализатор модели комментарий."""

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date', )
