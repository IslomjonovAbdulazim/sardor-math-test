import sqlite3
from datetime import datetime


class Results:
    def __init__(self, path_to_db="results.db"):
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
            id varchar(50) NOT NULL,
            correct int NOT NULL,
            wrong NOT NULL,
            not_selected NOT NULL,
            user varchar(30) NOT NULL,
            test int NOT NULL,
            start timestamp NOT NULL,
            end timestamp NOT NULL,
            answers varchar(200) NOT NULL,
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    def update_user_answers(self, answers, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET answers=? WHERE id=?
        """
        return self.execute(sql, parameters=(answers, id), commit=True)

    def update_user_end(self, end, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET end=? WHERE id=?
        """
        return self.execute(sql, parameters=(end, id), commit=True)

    def update_user_corrects(self, correct, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET correct=? WHERE id=?
        """
        return self.execute(sql, parameters=(correct, id), commit=True)

    def update_user_wrongs(self, wrongs, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET wrong=? WHERE id=?
        """
        return self.execute(sql, parameters=(wrongs, id), commit=True)

    def update_user_not_selected(self, not_selected, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET not_selected=? WHERE id=?
        """
        return self.execute(sql, parameters=(not_selected, id), commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: str, correct: int, wrong: int, not_selected: int, user: str, test: int, start: datetime,
                 end: datetime, answers: str):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Users(id, correct, wrong, not_selected, user, test, start, end, answers) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(
            id, correct, wrong, not_selected, user, test, start.timestamp(), end.timestamp(), answers),
                     commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
