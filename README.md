# api_yamdb

 Командный проект YaMDb.\
Собирает отзывы пользователей на произведения. Произведения делятся на категории.
Сами произведения в YaMDb не хранятся. Произведению может быть присвоен жанр из списка предустановленных.
Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку; 
из пользовательских оценок формируется рейтинг.

![example workflow](https://github.com/heydolono/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Технологии
- [Django] - Бэкэнд фреймворк
- [Django Rest Framework] - Фрэймворк для создания API на основе Django
- [Django REST Framework Simple JWT] - Библиотека для авторизации с помощью JWT-токенов
- [Django Filter] - Библиотека для фильтрации данных

## Шаблон наполнения env-файла
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 
```
## Установка

### Запуск приложения в контейнерах:
```
docker-compose up
```
### Выполнить миграции:
```
docker-compose exec web python manage.py migrate
```
### Создать суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```
### Резервная копия БД
```
docker-compose exec web python manage.py dumpdata > fixtures.json
```
### Заполнение БД из файла фикстур
```
docker-compose exec web python manage.py loaddata fixtures.json
```
### Загрузка статики:
```
docker-compose exec web python manage.py collectstatic --no-input
```

## Примеры запросов к API и ответов
### Доступно на http://127.0.0.1:8000/redoc/

### Развернутый проект доступен на http://<ipсервера>

[//]: # 

   [Django]: <https://www.djangoproject.com>
   [Django Rest Framework]: <https://www.django-rest-framework.org>
   [Django REST Framework Simple JWT]: <https://github.com/jazzband/djangorestframework-simplejwt>
   [Django Filter]: <https://github.com/carltongibson/django-filter>

## Разработчики
- [Пётр Чухланцев](https://github.com/PETRUSHQUE)
- [Максим Колесников](https://github.com/heydolono)
- [Александр Шевченко](https://github.com/Persev88)

