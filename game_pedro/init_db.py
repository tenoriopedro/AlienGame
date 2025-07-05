import mysql.connector
import os
import dotenv


class GameDB:
    # Database creation

    def __init__(self):

        dotenv.load_dotenv()
        self.create_database()
        self.conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DATABASE_NAME"),
        )
        self.create_table()

    def create_database(self):
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )

        cursor = conn.cursor()
        cursor.execute(
            f'CREATE DATABASE IF NOT EXISTS {os.getenv("DATABASE_NAME")}'
            )

        conn.commit()
        cursor.close()
        conn.close()

    def create_table(self):
        cursor = self.conn.cursor()

        cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {os.getenv("TABLE")} ('
            'id INT NOT NULL AUTO_INCREMENT, '
            'score INT NOT NULL, '
            'PRIMARY KEY (id)'
            ') '
        )

        self.conn.commit()
        cursor.close()

    def collect_data(self, score):
        cursor = self.conn.cursor()

        sql = f'INSERT INTO {os.getenv("TABLE")} (score) VALUES (%s)'
        value = score,
        
        cursor.execute(sql, value)

        self.conn.commit()
        cursor.close()

    def get_max_score(self):

        cursor = self.conn.cursor()

        sql = f' SELECT MAX(score) FROM {os.getenv("TABLE")}'
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()

        return result[0] if result else 0

    def close_connection(self):
        if self.conn.is_connected():
            self.conn.close()