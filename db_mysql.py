# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, line-too-long

import json
import mysql.connector as mysql


class Mysqldatabase:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None


    def create_connection(self):
        conn = None
        try:
            conn = mysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password, database=MYSQL_DATABASE)
        except mysql.Error as err:
            print(err)

        self.connection = conn


    def create_table(self, create_table_sql: str):
        self.create_connection()
        if bool(self.connection):
            try:
                cur = self.connection.cursor()
                cur.execute(create_table_sql)
            except mysql.Error as err:
                print(err)
        else:
            print("Error! Cannot create the database connection.")
        self.connection.close()


    def create_tables(self, tables_json):
        tables = json.loads(tables_json)

        for table in tables:
            self.create_table(self.generate_sql(table))


    def generate_sql(self, table_dict) -> str:
        table_name = table_dict["table_name"]
        columns = table_dict["columns"]
        segments = []
        table_columns = []
        constraints = []
        primary_key = []
        unique = []

        for column in columns:
            not_null = ""
            if bool(column["not_null"]):
                not_null = "NOT NULL"

            auto_increment = ""
            if bool(column["auto_increment"]):
                auto_increment = "AUTO_INCREMENT"

            if bool(column["unique"]):
                unique.append(column['name'])

            if bool(column["primary_key"]):
                primary_key.append(column['name'])

            table_columns.append(f"{column['name']} {column['datatype']} {not_null} {auto_increment}".strip())

        if bool(primary_key):
            if len(primary_key) == 1:
                constraints.append(f"PRIMARY KEY ({primary_key[0]})")
            else:
                constraints.append(f"CONSTRAINT PK_{table_name} PRIMARY KEY ({', '.join(primary_key)})")

        if bool(unique):
            if len(unique) == 1:
                constraints.append(f"UNIQUE ({unique[0]})")
            else:
                constraints.append(f"CONSTRAINT UC_{table_name} UNIQUE ({', '.join(unique)})")

        segments.append(', '.join(table_columns))
        segments.append(', '.join(constraints))

        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(segments)});"

        return sql


    def data_insert(self, table: str, **values) -> int:
        column_names = ', '.join(values.keys())
        column_values = ', '.join(['%s'] * len(values))
        sql = f"INSERT INTO {table} ({column_names}) VALUES ({column_values})"
        # print(sql, tuple(values.values()))
        ret = None

        self.create_connection()
        if bool(self.connection):
            try:
                cur = self.connection.cursor()
                cur.execute(sql, tuple(values.values()))
                self.connection.commit()
                ret = cur.lastrowid
            except mysql.Error as err:
                print(err)
        else:
            print("Error! Cannot create the database connection.")
        self.connection.close()

        return ret


    def data_select(self, table: str, fields: tuple = ("*",), where_clause: str = None) -> list:
        ret = None

        select_fields = ','.join(fields)
        sql = f"SELECT {select_fields} FROM {table}"

        if bool(where_clause):
            sql += f" WHERE {where_clause}"

        self.create_connection()
        if bool(self.connection):
            try:
                cur = self.connection.cursor()
                cur.execute(sql)
                ret = cur.fetchall()
            except mysql.Error as err:
                print(err)
        else:
            print("Error! Cannot create the database connection.")
        self.connection.close()

        return ret
