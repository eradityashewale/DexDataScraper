import psycopg2
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

host = config['PostgreSQL']['host']
dbname = config['PostgreSQL']['dbname']
user = config['PostgreSQL']['user']
password = config['PostgreSQL']['password']
port = config['PostgreSQL']['port']

class DBConnector():

    def __init__(self):
        self.dbconn = None

    def create_connection(self):
        try:
            connection = psycopg2.connect(
                host=host, 
                dbname=dbname, 
                user=user, 
                password=password, 
                port=port)
            return connection
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None

    def __enter__(self):
        self.dbconn = self.create_connection()
        return self.dbconn
    
    def __exit__(self):
        self.dbconn.close()

class DBConnection(object):
    connection = None

    @classmethod
    def get_connection(cls, new=False):
        return DBConnector().create_connection()
    

