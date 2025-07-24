# Django REST Framework + Vue.js Project

## Описание

Динамическая лента коментариев с бэкендом на DRF и фронтендом на Vue.js.  
Бэкенд предоставляет REST API, фронтенд работает через axios с этим API.

---

## Технологии

### Backend
- Python 3.x
- Django
- Django REST Framework
- PostgreSQL (или SQLite)
- Channels

### Frontend
- Vue 3
- Vuex
- Axios
- Bootstrap

### Прочие
- Google reCAPTCHA v2
- FingerprintJS
- Docker
- Docker Compose

---

## Установка и запуск проекта

### Для разработки

Клонируйте репозиторий:

``` bash
git clone https://github.com/fe7h/ComentsTestTask.git
cd ComentsTestTask
```

Создайте виртуальное окружение:

``` bash
python -m venv venv
source venv/bin/activate 
```

Установите зависимости:

``` bash
pip install -r backend/requirements.txt
npm install --prefix ./frontend
```

Выполните миграции базы данных:

``` bash
python3 backend/manage.py migrate
```

Запустите оба сервера:

``` bash
python3 backend/manage.py runserver
npm run dev --prefix ./frontend
```

### В продакшн 

Клонируйте репозиторий:

``` bash
git clone https://github.com/fe7h/ComentsTestTask.git
cd ComentsTestTask
```
Заполните необходимые поля в:

- `.env`
- `init.sql`
- `frontend/src/store/index.js`

[Установите](https://docs.docker.com/engine/install/ubuntu/) `docker` и `docker compose`.

Соберите контейнеры:

``` bash
sudo docker compose up -d --build
```

---

## Об проекте

Лента комментариев с возможностью оставлять ответы. 

### Модели

- `BaseComment, TopComment, NestedComment`

Модель комментариев реализована с использованием `django-polymorphic`, 
что позволяет разделить логику вложенных и не вложенных комментариев при 
этом оставив им единый интерфейс.

Так же с помощью `django-cte` реализован менеджер модели возвращающий 
всех её наследников (используется только в админке).

- `AttachedMedia, AttachedFile, AttachedImage`

Модель для медиа так же реализована через `django-polymorphic` — 
это позволило упростить логику полей модели комментариев.

- `UserData`

Модель, что хранит в себе данные генерируемые с помощью `FingerprintJS`.
Уникальный хеш пользователя создается на стороне модели.

### API

Все `GET` запросы к базе данных через api **оптимизированы до O(1)** — независимо от глубины вложенности.

Для возможности межсайтовых запросов используется `django-cors-headers`.

### WebSocket

Реализован с помощью `channels`, как сервер стоит `daphne`. 

Фронтенд при входе на сайт устанавливает *WebSocket*-соединение, 
по которому отправляет *id* всех веток комментариев, 
которые отслеживает пользователь.

На бэкенде подключение обрабатывается через `consumer`. 
При создании нового комментария срабатывает сигнал. 
Если новый комментарий относится к одной из отслеживаемых веток, 
он отправляется пользователю через открытое *WebSocket*-соединение.

### Админка

- Настроено отображение всех моделей
- Добавлена возможность переходить по ссылкам от модели к модели
- Настроен фильтр возвращающий всех наследников комментария по его `id`

### Защита
- От **csrf** используется токен
- От **спама** Google reCAPTCHA v2 (checkbox)
- От **xss** экранируются все теги кроме разрешённых  

### Management

Команда заполняющая БД данными генерируемыми с помощью `Faker`.

``` bash
python3 manage.py comments_auto_populate
```
