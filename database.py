import psycopg2
from envs import environments as envs

class Databases():
    def __init__(self):
        self.db = psycopg2.connect(
            host=envs.POSTGRES_HOST,
            dbname=envs.POSTGRES_DB,
            user=envs.POSTGRES_USER,
            password=envs.POSTGRES_PASSWORD,
            port=5432
        )
        self.cursor = self.db.cursor()

    def close(self):
        self.cursor.close()
        self.db.close()

    def execute(self, query, args=None, fetch=True):
        self.cursor.execute(query, args or ())
        if fetch:
            return self.cursor.fetchall()
        self.db.commit()
        return None

    def commit(self):
        self.db.commit()
