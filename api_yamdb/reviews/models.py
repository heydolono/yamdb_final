from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_username, validate_year


class User(AbstractUser):
    """Класс модели пользователя."""

    ADMIN = 'admin'
    MODER = 'moderator'
    USER = 'user'
    ROLE_CHOICES = (
        (ADMIN, 'Админ'),
        (MODER, 'Модератор'),
        (USER, 'Пользователь'),
    )
    username = models.CharField(
        'Никнейм', unique=True, max_length=settings.USERNAME_LENGTH,
        validators=[validate_username])
    email = models.EmailField(
        'Почта', unique=True, max_length=settings.EMAIL_LENGTH)
    role = models.CharField(
        'Роль', choices=ROLE_CHOICES, default=USER,
        max_length=max(len(role) for role, _ in ROLE_CHOICES))
    first_name = models.CharField('Имя', blank=True, null=True, max_length=150)
    last_name = models.CharField(
        'Фамилия', blank=True, null=True, max_length=150)
    bio = models.TextField('Биография', blank=True, null=True, max_length=300)
    confirmation_code = models.CharField(
        'Код подтверждения', blank=True, null=True, default=None,
        max_length=settings.CODE_LENGTH)

    class Meta:
        ordering = ('username', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        """Метод проверки пользователя на наличие роли администратора."""
        return self.role == self.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        """Метод проверки пользователя на наличие роли модератора."""
        return self.role == self.MODER


class BaseSection(models.Model):
    """Базовый класс для моделей категория и жанр."""
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        abstract = True
        ordering = ('name', )

    def __str__(self):
        return self.name


class Category(BaseSection):
    """Класс модели категория."""

    class Meta(BaseSection.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseSection):
    """Класс модели категория."""

    class Meta(BaseSection.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Класс модели произведение."""
    name = models.CharField('Название произведения', max_length=256)
    year = models.IntegerField('Год выпуска', validators=[validate_year, ])
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles',
        null=True, verbose_name='Категория')
    description = models.TextField('Описание', blank=True, null=True)

    class Meta:
        ordering = ('-year', 'name', )
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name

    def get_genres(self):
        return '\n'.join([g.name for g in self.genre.all()])

    get_genres.short_description = 'Жанр'


class GenreTitle(models.Model):
    """Класс модели связи между произведениями и жанрами."""

    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    title = models.ForeignKey(Title, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Жанры произведений'
        verbose_name_plural = 'Жанры произведений'

    def __str__(self):
        return f'Жанр произведения {self.title} - {self.genre}.'


class BasePost(models.Model):
    """Базовый класс для моделей отзыв и комментарий."""
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='%(class)ss', verbose_name='Автор')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date', )
        abstract = True

    def __str__(self):
        return self.text[:30]


class Review(BasePost):
    """Класс модели отзыв."""
    score = models.IntegerField(
        default=0, validators=[MaxValueValidator(10), MinValueValidator(1)],
        verbose_name='Оценка')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews', verbose_name='Произведение')

    class Meta(BasePost.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title', ), name='unique_title_review')]


class Comment(BasePost):
    """Класс модели комментарий."""
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments', verbose_name='Отзыв')

    class Meta(BasePost.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
