from typing import Any

from sqlalchemy import create_engine, select, Engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker


class Database:
    __server: str = None
    __database: str = None
    __user: str = None
    __password: str = None
    __session: Session | Any = None
    __engine: Engine | None = None
    __connection_open: bool = False

    def __init__(self, config):
        self.__server = config.database['server']
        self.__database = config.database['database']
        self.__user = config.database['user']
        self.__password = config.database['password']

    def session(self) -> Session:
        if self.__session is None:
            self.__connect()
            if self.__lost_connection():
                self.__close_connection()
                self.__connect()
        return self.__session

    def __connect(self):
        self.__engine = create_engine(self.__connection_string())
        session = scoped_session(sessionmaker())
        self.__session = session
        session.configure(bind=self.__engine)
        self.__connection_open = True

    def __connection_string(self):
        return f'mssql+pymssql://{self.__user}:{self.__password}@{self.__server}/{self.__database}'

    def __lost_connection(self):
        invalidated = True
        if self.__session is not None:
            connection = self.__session.connection()
            try:
                connection.scalar(select([1]))
            except Exception:
                invalidated = connection.closed or connection.invalidated
        return invalidated

    def __close_connection(self):
        if self.__connection_open:
            if self.__session is not None:
                self.__session.close()
            if self.__engine is not None:
                self.__engine.dispose()
                self.__engine = None
