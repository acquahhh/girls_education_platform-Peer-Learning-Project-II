"""Database connection management for MySQL hosted on Aiven."""

import mysql.connector
from mysql.connector import Error

from config.settings import settings


class Database:
    """Manages a single MySQL connection and query execution."""

    def __init__(self):
        self._connection = None

    def connect(self):
        """Open a connection to the Aiven MySQL instance."""
        if self._connection and self._connection.is_connected():
            return self._connection

        settings.validate()

        connect_kwargs = {
            "host": settings.DB_HOST,
            "port": settings.DB_PORT,
            "database": settings.DB_NAME,
            "user": settings.DB_USER,
            "password": settings.DB_PASSWORD,
            "ssl_disabled": False,
        }
        if settings.DB_SSL_CA:
            connect_kwargs["ssl_ca"] = settings.DB_SSL_CA

        try:
            self._connection = mysql.connector.connect(**connect_kwargs)
            return self._connection
        except Error as exc:
            raise Error(f"Failed to connect to the database: {exc}")

    def get_connection(self):
        """Return an active connection, opening one if necessary."""
        if not self._connection or not self._connection.is_connected():
            return self.connect()
        return self._connection

    def execute(self, query, params=None, commit=False):
        """Execute a write query (INSERT/UPDATE/DELETE) safely."""
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query, params or ())
            if commit:
                connection.commit()
            return cursor.lastrowid if cursor.lastrowid else cursor.rowcount
        except Error as exc:
            connection.rollback()
            raise Error(f"Query failed and was rolled back: {exc}")
        finally:
            cursor.close()

    def fetch_one(self, query, params=None):
        """Run a SELECT and return a single row as a dict, or None."""
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            return cursor.fetchone()
        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        """Run a SELECT and return all rows as a list of dicts."""
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            return cursor.fetchall()
        finally:
            cursor.close()

    def fetch_scalar(self, query, params=None):
        """Run a SELECT that returns a single value (e.g. COUNT)."""
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query, params or ())
            row = cursor.fetchone()
            return row[0] if row else None
        finally:
            cursor.close()

    def close(self):
        """Close the connection if it is open."""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            self._connection = None


db = Database() 