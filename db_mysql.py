# pylint: disable=missing-module-docstring, missing-function-docstring, line-too-long

import mysql.connector as mysql
import settings


setting = settings.Settings()
MYSQL_HOST = setting.mysql_host
MYSQL_USER = setting.mysql_user
MYSQL_PASSWORD = setting.mysql_password
MYSQL_DATABASE = setting.mysql_database


def create_connection() -> mysql.MySQLConnection:
    conn = None
    try:
        conn = mysql.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, database=MYSQL_DATABASE)
    except mysql.Error as err:
        print(err)

    return conn


def create_table(create_table_sql: str):
    conn = create_connection()
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute(create_table_sql)
        except mysql.Error as err:
            print(err)
    else:
        print("Error! Cannot create the database connection.")
    conn.close()


def create_tables():
    sql_create_table_sensordata = """CREATE TABLE IF NOT EXISTS sensordata (
                                        id int(11) NOT NULL AUTO_INCREMENT,
                                        sensorid text NOT NULL,
                                        datetime datetime NOT NULL,
                                        location text,
                                        sensorType text NOT NULL,
                                        unit text,
                                        value double NOT NULL,
                                        PRIMARY KEY (id)
                                    );"""

    create_table(sql_create_table_sensordata)


def data_insert(table: str, **values) -> int:
    column_names = ', '.join(values.keys())
    column_values = ', '.join(['%s'] * len(values))
    sql = f"INSERT INTO {table} ({column_names}) VALUES ({column_values})"
    # print(sql, tuple(values.values()))
    ret = None

    conn = create_connection()
    if bool(conn):
        try:
            cur = conn.cursor()
            cur.execute(sql, tuple(values.values()))
            conn.commit()
            ret = cur.lastrowid
        except mysql.Error as err:
            print(err)
    else:
        print("Error! Cannot create the database connection.")
    conn.close()

    return ret


def data_select(table: str, fields: tuple = ("*",), where_clause: str = None) -> list:
    ret = None

    select_fields = ','.join(fields)
    sql = f"SELECT {select_fields} FROM {table}"

    if bool(where_clause):
        sql += f" WHERE {where_clause}"

    conn = create_connection()
    if bool(conn):
        try:
            cur = conn.cursor()
            cur.execute(sql)
            ret = cur.fetchall()
        except mysql.Error as err:
            print(err)
    else:
        print("Error! Cannot create the database connection.")
    conn.close()

    return ret
