[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

# «Продуктовый помощник» 

#### _Описание_

Онлайн-сервис публикации рецептов. Пользователь имеет возможность подписываться на рецепты других пользователей, добавлять понравившиеся рецепты в список "Избранное" или в "Список покупок", чтобы купить необходимые продукты в нужном количестве.

##### Запуск (docker)

Выполнить команду docker-compose up из директории backend/foodgram_:

_docker-compose up -d_

Выполнить команду docker-compose up из директории frontend/:

_docker-compose up -d_

В терминале выполнить следующие команды:

_docker exec -it foodgram_project bash_

Cоздать суперпользователя:

_python manage.py createsuperuser_

Ввести имя пользователя и пароль.

Загрузить ингредиенты:

_python manage.py shell_
_>>>from utils.upload_ingredients import upload_ingredients_
_>>> upload_ingredients()_

По http://51.250.70.83/ доступна страница входа на сайт.

По http://51.250.70.83:8081/admin доступна страница администрирования. 
Данные для суперпользователя:
Логин: Review
Пароль: 12345