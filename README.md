Для запуска проекта необходимо выполнить команду: 

docker-compose 

build docker-compose up

После успешного запуска, API будет доступно по следующему адресу:

[http://localhost:60102/api/v1](http://localhost:60102/api/v1)

Документация к API доступна по адресу:

[http://localhost:60102/docs](http://localhost:60102/docs)

Веб-интерфейс доступен по адресу:

[http://localhost:60102/web/posts](http://localhost:60102/web/posts)

# Реализация
## База данных
Таблицы описаннны в [Db_objects.py](database%2FDb_objects.py) в виде объектов sqlalchemy.

Логика работы с базой данных описана в классе DataBase в модуле [async_db.py](database%2Fasync_db.py). Предполагается
использовать его через объект db в данном модуле.

## Сервер

Общая настройка сервера находиться в [app.py](app%2Fapp.py)

Сервер имеет 3 модуля:
### Токен
[token.py](app%2Frouters%2Ftoken.py) в данном модуле описывается методы получения токена и его обработки.

### API
[api.py](app%2Frouters%2Fapi.py) в данном модуле описывается работа api.

### WEB
[web.py](app%2Frouters%2Fweb.py) в данном модуле описывается работа с web интерфейсом.
