# Практика написания API с использованием FastAPI
## Установка и запуск
### Конфигурация
Создайте .env файл в корне проекта (пример .env файла - .env.example) <br>
В нем нужно указать значения:<br>
- JWT_SECRET_KEY (секретный ключ для генерации jwt токена)<br>
- DB_NAME (имя базы данных)
- DB_HOST (хост базы данных)
- DB_USER (имя пользователя базы данных)
- DB_PASS (пароль базы данных, по умолчанию - password)
- DB_PORT (порт базы данных)
- ACCESS_TOKEN_EXPIRE_MINUTES (время валидности access токена в минутах)
- REFRESH_TOKEN_EXPIRE_MINUTES (время валидности refresh токена в минутах)
### Установить Docker и запустить его
Установить Docker можно по ссылке: https://docs.docker.com/get-docker/
### Перейти в папку auth_service
```
cd auth_service
```
### Запустить проект
```
docker compose up --build
```