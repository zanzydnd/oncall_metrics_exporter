# SRE 4-th ASSIGMENT
Контекст: бизнес

Индикаторы:
 - Кол-во дней в течении сл 30 дней, в которых нет ни одного пользователя с primary ролью
 - Кол-во юзеров , у которых не включены уведмоления на primary роль.


Бизнес
```
Кол-во юзеров , у которых не включены уведмоления на primary роль < 15% от общего кол-ва в базе
Кол-во дней в течении сл 30 дней, в которых нет ни одного пользователя с primary ролью не превышает 2 дней
```
Системные
```
Кол-во внутренних ошибок не должно быть выше 2%
Сервис должен отвечать < 2c. в 95% случаев
```
Установка:
```sh
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Запуск:
```sh 
python3 -m src
```