# Импортировать пакет psycopg2
# docker exec -it postgres-C4sT psql -U postgres (команда для работы с psql)

import psycopg2

# Открыть подключение к базе.
# Обратите внимание на синтаксис строки с информацией о БД:
# если вы меняли настройки своей БД, то и здесь их придется
# указать соответствующие.
# Кстати, таких подключений можно открывать сколько угодно:
# вдруг у вашего приложения данные распределены
# по нескольким базам?
conn = psycopg2.connect(
    "dbname=postgres user=postgres password=postgrespw"
)

# Создать «курсор» на подключении к базе.
# Курсоры используются для представления
# сессий подключения к БД.
cur = conn.cursor()

# Выполнить команду напрямую.
cur.execute(
    "CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);"
)

# Выполнить команду, не заботясь о корректном синтаксисе
# представления данных: psycopg2 всё сделает за нас.
cur.execute(
    "INSERT INTO test (num, data) VALUES (%s, %s)",
    (100, "abc'def")
)

# Выполнить команду
cur.execute("SELECT * FROM test;")
# Но как получить результат её выполнения?..

# А вот так. fetchone — «принести» одну строчку результата,
# fetchall — все строчки.
cur.fetchone()

# Завершить транзакцию
conn.commit()
# Закрыть курсор
cur.close()
# Закрыть подключение
conn.close()