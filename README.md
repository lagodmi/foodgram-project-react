# Foodgram — продуктовый помощник.
## Описание проекта:
- Сайт имеет полный функционал по авторизации, авторизованные пользователи могут выставлять свои рецепты, подписываться на других пользователей, добавлять рецепты в избранное, создавать свой список покупок.
## Стек проекта:
- Python 3.9
- Django 3.2.3
- Django REST framework 3.12.4
- JavaScript
## Cсылка на развернутый проект:
- http://84.252.142.240:5000
- foodgram.3utilities.com/signin
## Процесс запуска проекта (через docker compose):
### Какую версию развернуть:
- В случае развертывания проекта в производственной среде следует использовать docker-compose.production.yml.
- Для разработки, тестирования или демонстрации концепции docker-compose.yml.
### Запуск проекта:
- Клонируем репозиторий:
    https://github.com/lagodmi/foodgram-project-react.git
- Создаем файл .env в корне проекта c параметрами указанными в .env.example:
    nano .env
- Выполняем запуск:
    docker compose -f docker-compose.yml up -d
- Заходим в интерактивный терминал backend и выполняем команды:
    - docker compose exec -it backend bash
        - python manage.py migrate
        - python manage.py loaddb
        - python manage.py collectstatic
        - cp -r /app/collected_static/. /backend_static/static/
- Проект доступен на:
    http://localhost:8000/
### Пример запросов:
- Cтраница аутентификации:
    http://localhost:8000/signin
- Страница рецептов:
    http://localhost:8000/recipes
- Страница подписок:
    http://localhost:8000/subscriptions
- Страница создания рецепта:
    http://localhost:8000/recipes/create
- Страница избранных рецептов:
    http://localhost:8000/favorites
- Страница списка покупок:
    http://localhost:8000/cart
## Автор проекта:
Лагоднов Д.С.
