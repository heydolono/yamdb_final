from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Category, Comment, Genre, GenreTitle, Review, Title, User


@admin.register(User)
class UserAdmin(UserAdmin):
    """Класс админки для модели пользователя."""
    model = User
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = (
        'username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'role', )
    empty_value_display = '-пусто-'
    fieldsets = (
        (None, {'fields': ('username', 'role', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email',
                                         'bio')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Класс админки для модели произведение."""
    list_display = (
        'id', 'name', 'year', 'description', 'category', 'get_genres', )
    search_fields = ('name',)
    list_filter = ('name', 'year', 'genre', 'category', )
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Класс админки для модели категория."""
    list_display = ('id', 'name', 'slug', )
    search_fields = ('name', )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Класс админки для модели жанр."""
    list_display = ('id', 'name', 'slug', )
    search_fields = ('name', )


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    """Класс админки для модели жанр произведений."""
    list_display = ('genre', 'title', )
    search_fields = ('name',)
    list_filter = (
        'genre',
        'title',
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Класс админки для модели отзыв."""
    list_display = ('text', 'author', 'score', 'pub_date', 'title', )
    search_fields = ('text', 'author', 'title', )
    list_filter = ('pub_date', 'author', 'score', 'title', )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Класс админки для модели комментарий."""
    list_display = ('text', 'author', 'review', 'pub_date', )
    search_fields = ('text', 'author', )
    list_filter = ('pub_date', 'author', )
