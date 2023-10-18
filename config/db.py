from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv
import os


_ = load_dotenv(find_dotenv())

db_host = os.getenv("db_host")
db_port = os.getenv("db_port")
db_username = os.getenv("db_username")
db_password = os.getenv("db_password")
db_name = os.getenv("db_name")

MYSQL_URL = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8"

POOL_SIZE = 20
POOL_RECYCLE = 3600
POOL_TIMEOUT = 15
MAX_OVERFLOW = 2
CONNECT_TIMEOUT = 60

class Database():
    def __init__(self) -> None:
        self.connection_is_active = False
        self.engine = None

    def get_db_connection(self):
        if self.connection_is_active == False:
            connect_args = {"connect_timeout":CONNECT_TIMEOUT}
            try:
                self.engine = create_engine(MYSQL_URL, pool_size=POOL_SIZE, pool_recycle=POOL_RECYCLE,
                        pool_timeout=POOL_TIMEOUT, max_overflow=MAX_OVERFLOW, connect_args=connect_args)
                return self.engine
            except Exception as ex:
                print("Error connecting to DB : ", ex)
        return self.engine

    def get_db_session(self,engine):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            return session
        except Exception as ex:
            print("Error getting DB session : ", ex)
            return None