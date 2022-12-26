from django_filters.rest_framework import (
    CharFilter, FilterSet, ModelMultipleChoiceFilter)

from reviews.models import Category, Genre, Title


class TitleFilter(FilterSet):
    """Класс фильтра для модели произведение."""
    category = ModelMultipleChoiceFilter(
        field_name='category__slug', to_field_name='slug',
        queryset=Category.objects.all())
    genre = ModelMultipleChoiceFilter(
        field_name='genre__slug', to_field_name='slug',
        queryset=Genre.objects.all())
    name = CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year', )
