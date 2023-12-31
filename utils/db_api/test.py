import calendar
from datetime import time, date, datetime
import sqlite3


class DatabaseTest:

    def __init__(self, path_to_db="test.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int NOT NULL,
            media varchar(1000) NOT NULL,
            answers varchar(256) NOT NULL,
            start timestamp not null,
            end timestamp not null,
            time int not null,
            PRIMARY KEY (id)
        );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, media: str, answers: str, start: datetime, end: datetime, t: int):
        sql = """
        INSERT INTO Users(id, media, answers, start, end, time) VALUES (?,?,?,?,?,?)
        """
        self.execute(sql, parameters=(id, media, answers, start.timestamp(), end.timestamp(), t), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_answers(self, answers, id):
        sql = f"""
        UPDATE Users SET answers=? WHERE id=?
        """
        return self.execute(sql, parameters=(answers, id), commit=True)

    def update_user_start(self, time, id):
        sql = f"""
        UPDATE Users SET start=? WHERE id=?
        """
        return self.execute(sql, parameters=(time, id), commit=True)

    def update_user_end(self, time, id):
        sql = f"""
        UPDATE Users SET end=? WHERE id=?
        """
        return self.execute(sql, parameters=(time, id), commit=True)

    def update_user_time(self, time, id):
        sql = f"""
        UPDATE Users SET time=? WHERE id=?
        """
        return self.execute(sql, parameters=(time, id), commit=True)

    def delete_users(self):
        self.execute("delete from Users where TRUE", commit=True)


def logger(statement):
    print(f"""
    -----------------------------------------------
    Executing:
    {statement}
    -----------------------------------------------
    """)
