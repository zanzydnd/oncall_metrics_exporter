# SRE 4-th ASSIGMENT
Контекст: бизнес

Индикаторы:
 - Кол-во дней в течении сл 30 дней, в которых нет ни одного пользователя с primary ролью
 - Кол-во юзеров , у которых не включены уведмоления на primary роль.


Бизнес
```
Кол-во юзеров , у которых не включены уведмоления на primary роль
SLO :< 15% от общего кол-ва в базе
Кол-во дней в течении сл 30 дней, в которых нет ни одного пользователя с primary 
ролью не превышает 4 дней. 
SLO: <~15% дней могут не иметь кого-то на primary роли
```
Системные
```
Кол-во внутренних ошибок 
SLO: не должно быть выше 2% (все 5** статусы)
Сервис должен отвечать < 2c. 
SLO: время ответов в 95% случаев не превышает 2с 
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