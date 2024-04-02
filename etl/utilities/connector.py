from dotenv import load_dotenv
import os
import clickhouse_connect

class ConnectToDatabase:

    def __init__(self) -> None:
        load_dotenv()
        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT')
        self.username = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        # self.db = os.getenv('DB_NAME')
        self.conn = None

    def connect(self):
        try:
            self.conn = clickhouse_connect.get_client(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password)
                # database=self.db)
            print('Database Connected ...!')
        except ConnectionError as err:
            print('Database Connection Failed !!', err)

        return self.conn
