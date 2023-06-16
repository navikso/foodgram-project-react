[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

# «Продуктовый помощник» 

#### _Описание_

Онлайн-сервис публикации рецептов. Пользователь имеет возможность подписываться на рецепты других пользователей, добавлять понравившиеся рецепты в список "Избранное" или в "Список покупок", чтобы купить необходимые продукты в нужном количестве.

##### Запуск (docker)

Запустить docker-compose:

_docker-compose up_

Выполнить миграции:

_docker-compose exec web python manage.py migrate_

Загрузить список ингредиентов:

_docker-compose exec web python manage.py loaddata ingredients.json_
