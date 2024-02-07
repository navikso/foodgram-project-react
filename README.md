# «Продуктовый помощник» 

#### _Описание_

Онлайн-сервис публикации рецептов. Пользователь имеет возможность подписываться на рецепты других пользователей, добавлять понравившиеся рецепты в список "Избранное" или в "Список покупок", чтобы купить необходимые продукты в нужном количестве.

##### Запуск (docker)

На примере env_example создайте и заполните файл .env  

Выполнить команды docker-compose up из директории backend/foodgram_:

`docker network create  mynetwork`

`docker-compose up -d`

Выполнить команду docker-compose up из директории frontend/:

`docker-compose up -d`

В терминале выполнить следующие команды:

`docker exec -it foodgram_project bash`

Cоздать суперпользователя:

`python manage.py createsuperuser`

Ввести имя пользователя и пароль.

#####Примеры запросов:

По http://158.160.37.68/ доступна страница входа на сайт.

http://158.160.37.68/recipes - главная страница с рецептами всех авторов, упорядоченными по дате добавления

http://158.160.37.68/users/1 - профиль пользователя с id=1

http://158.160.37.68/tags - страница с перечнем всех доступных тегов рецептов


_Администрирование:_

По http://158.160.37.68:8081/admin доступна страница администрирования. 

Данные суперпользователя:
Логин: root
Пароль: 1234

##### Об авторе:
Автор - Соколова Анастасия,
студентка курса "Python-разработчик плюс" от Яндекс.Практикум.
