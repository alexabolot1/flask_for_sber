# Ресурсы
import json

import pandas as pd
from flask_restful import Resource
from psycopg2.extras import RealDictCursor
import psycopg2

from app import DataTable


class DataListResourceSql(Resource):
    """
    Ресурс подключается к БД, создает новую колонку и добавляет новое поле 'deltalag' с интервалом - 2 месяца.
    После чего присвает переменной 'result' результат выполнения
    SQL-запроса, далее поле 'deltalag' удаляется. (Используются только SQL-запросы)
    """

    def get(self):
        con = psycopg2.connect(
            database="test",
            user="test",
            password="test",
            host="127.0.0.1",
            port="5433"
        )

        cur = con.cursor(cursor_factory=RealDictCursor)
        # Добавляем в таблицу новое поле datalag со смещением в - 2 месяца от поля rep_dt
        cur.execute("ALTER TABLE data_table DROP COLUMN if exists deltalag;"
                    "ALTER TABLE data_table ADD COLUMN deltalag date;"
                    "UPDATE data_table SET deltalag = rep_dt - INTERVAL '2 MONTH';"
                    )
        con.commit()
        cur.execute("SELECT * FROM data_table;")
        # Получаем в переменную result данные для вывода пользователю
        result = cur.fetchall()
        # Удаляем поле deltalag за ненадобностью.
        cur.execute("ALTER TABLE data_table DROP COLUMN if exists deltalag;")
        con.commit()
        con.close()
        return json.dumps(result, default=str)


class DataListResourcePandas(Resource):
    """
    Ресурс инициализирует пустой список данных, после чего в итеррируется по БД, затем добавляет
    словарь с данными в ранее пустой список, новое поле при этом в БД не создается.
    Смещение - 2 месяца реалзизуется с помощью библиотеки pandas.
    """

    def get(self):
        # создаем пустой список
        data_list = []
        # получаем данные из БД
        data = DataTable.query.all()
        # обходим данные формируя словрь для вывода результата
        for dt in data:
            data_dict = {
                'id': dt.id,
                'rep_dt': dt.rep_dt,
                'delta': dt.delta,
                'deltalag': dt.rep_dt - pd.DateOffset(months=2)
            }
            data_list.append(data_dict)
        return json.dumps(data_list, default=str)
