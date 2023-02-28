# Foodgram - Продуктовый помощник
# Ссылка на проект: http://51.250.84.193/recipes
Админка: http://51.250.84.193/admin
email: admin@gmail.com

![Build Status](https://github.com/Stanislav-Gutnikov/foodgram-project-react/workflows/tests/badge.svg)](https://github.com/Stanislav-Gutnikov/foodgram-project-react/actions/workflows/main.yml)

# Описание:

Учебный проект. API для сервиса продуктового помощника. Что умеет:

Публиковать рецепты
Добавлять рецепты в избранное
Составлять список покупок понравившегося рецепта
Скачивать список покупок
Подписываться и отписываться на определенного пользователя
Весь функционал проекта доступен только если пользователь зарегистрирован. Аутентификация реализована с помощью токена.

# Установка:

Клонируем репозиторий:

```
git clone git@github.com:Stanislav-Gutnikov/foodgram-project-react.git
```

Обновляем пакетный менеджер pip:

```
pip install --upgrade pip
```

Устанавливаем зависимости:

```
pip install -r requirements.txt
```

Собираем и запускаем проект:

```
docker-compose up -d --build
```

Устанавливаем миграций:

```
docker-compose exec backend python manage.py migrate
```

Создаем суперпользователя (администратора):

```
docker-compose exec backend python manage.py createsuperuser
```

Подключаем статику:

```
docker-compose exec backend python manage.py collectstatic --no-input
```

Наполняем базу данных ингредиентами:

```
docker-compose exec backend python manage.py loaddata ingred.json
```

# Шаблон .env файла (создать и заполнить .env для работы с БД):
DB_ENGINE=your_engine (работае с postgresql)
DB_NAME=your_name (имя базы данных)
POSTGRES_USER=your_user (логин для подключения к базе данных)
POSTGRES_PASSWORD=your_password (пароль для подключения к БД)
DB_HOST=your_host (название контейнера)
DB_PORT=your_port (порт для подключения к БД)