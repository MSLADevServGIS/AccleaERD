"""Database Connections
Author: Garin Wally; 5/3/2023

Yeah, database connection credentials in plain-text.
These are read-only accounts, so I'm not worried.
"""
import abc
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

ACCELA_DIALECT = "mssql+pyodbc"
ACCELA_DRIVER = "ODBC Driver 17 for SQL Server"
ACCELA_PORT = "14332"

# Force load the .env file from whatever the current directory
path = Path(__file__).parent.joinpath(".env")
load_dotenv(path)


class AbstractConnector(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def make_url(cls):
        """Placeholder for method of concrete classes."""
        pass

    @classmethod
    def connect(cls):
        """Return a connection engine."""
        connect_url = cls.make_url()
        engine = create_engine(connect_url)
        pd.read_sql("SELECT 'OK'", engine)  # Because pool_pre_ping=True doesn't seem to work
        return engine


class SQLiteConnector(AbstractConnector):
    """SQLite DB Connector (mostly for testing)."""
    connection_string = "sqlite:///"

    @classmethod
    def make_url(cls):
        return cls.connection_string


class BaseConnector(AbstractConnector):
    """Connection Base Class."""
    @classmethod
    def make_url(cls):
        """Return the connection string (URI)."""
        connect_url = URL.create(
            cls.dialect,
            username=cls.credentials.get("username", None),
            password=cls.credentials.get("password", None),
            host=cls.credentials.get("host", None),
            port=cls.credentials.get("port", None),
            database=cls.credentials.get("database", None),
            query=dict(driver=cls.driver)
            )
        return connect_url


class OldAccela(AbstractConnector):
    @classmethod
    def make_url(cls):
        return os.getenv("OLD_ACCELA")


class AccelaProd(BaseConnector):
    """Prod"""
    dialect = ACCELA_DIALECT
    driver = ACCELA_DRIVER
    credentials = {
        "username": os.environ["ACCELA_PROD_USERNAME"],
        "password": os.environ["ACCELA_PROD_PWD"],
        "host": os.environ["ACCELA_PROD_HOST"],
        "database": os.environ["ACCELA_PROD_DB"],
        "port": ACCELA_PORT
    }


class AccelaNonProd1(BaseConnector):
    """NonProd1"""
    dialect = ACCELA_DIALECT
    driver = ACCELA_DRIVER
    credentials = {
        "username": os.environ["ACCELA_NONPROD1_USERNAME"],
        "password": os.environ["ACCELA_NONPROD1_PWD"],
        "host": os.environ["ACCELA_NONPROD1_HOST"],
        "database": os.environ["ACCELA_NONPROD1_DB"],
        "port": ACCELA_PORT
    }


class AccelaNonProd2(BaseConnector):
    """NonProd2"""
    dialect = ACCELA_DIALECT
    driver = ACCELA_DRIVER
    credentials = {
        "username": os.environ["ACCELA_NONPROD2_USERNAME"],
        "password": os.environ["ACCELA_NONPROD2_PWD"],
        "host": os.environ["ACCELA_NONPROD2_HOST"],
        "database": os.environ["ACCELA_NONPROD2_DB"],
        "port": ACCELA_PORT
    }
