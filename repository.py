import atexit
import sqlite3
from dao import Dao
from dto import Hat
from dto import Supplier
from dto import Order


class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self.hats = Dao(Hat, self._conn)
        self.suppliers = Dao(Supplier, self._conn)
        self.orders = Dao(Order, self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE IF NOT EXISTS hats (
            id         INT      PRIMARY KEY,
            topping    TEXT     NOT NULL,
            supplier   INT      NOT NULL,
            quantity   INT      NOT NULL,
            
            FOREIGN KEY(supplier)      REFERENCES suppliers(id)

        );

        CREATE TABLE IF NOT EXISTS suppliers (
            id       INT     PRIMARY KEY,
            name     TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS orders (
            id        INT      PRIMARY KEY,
            location  TEXT     NOT NULL,
            hat       INT      NOT NULL,
            
            FOREIGN KEY(hat)   REFERENCES hats(id)

        );
    """)


# the repository singleton
repo = _Repository()
atexit.register(repo._close)
