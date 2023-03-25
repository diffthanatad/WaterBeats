import simplejson as json
import psycopg2
from psycopg2.extras import RealDictCursor

class PostgresWrapper:

    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = self.connect()

    def connect(self):
        pg_conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.connection = pg_conn

    def get_json_cursor(self):
        return self.connection.cursor(cursor_factory=RealDictCursor)

    def execute_and_fetch(self, query):
        cursor = self.get_json_cursor()
        cursor.execute(query)
        response = cursor.fetchall()

        cursor.close()
        return json.dumps(response)