import mysql.connector
import os
import dotenv


class GameDB:
    # Database creation

    def __init__(self):

        dotenv.load_dotenv()
        self.create_database()
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
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DATABASE_NAME"),
        )

        cursor = conn.cursor()
        cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {os.getenv("TABLE")} ('
            'id INT NOT NULL AUTO_INCREMENT, '
            'score INT NOT NULL, '
            'PRIMARY KEY (id)'
            ') '
        )

        conn.commit()
        cursor.close()
        conn.close()

