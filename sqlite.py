__author__ = 'Davide Monfrecola'

import random
import unittest
import os

from monitors.sqlitemanager import SqliteConnector

class TestSqlite(unittest.TestCase):

    def setUp(self):
        self.sqlite = SqliteConnector("test.db")
        self.sqlite.connect()

    def test_sqlite_connector(self):
        print("Create table test")
        self.sqlite.create("test", "test1 text, test2 text")
        print("Insert some data")
        self.sqlite.insert("test", "'1', '2'")
        self.sqlite.insert("test", "'3', '4'")
        self.sqlite.insert("test", "'5', '6'")
        self.sqlite.print_all("test")
        print("Update test2 where test1 = 1")
        self.sqlite.update("test", "test2='updated'", "test1='1'")
        self.sqlite.print_all("test")
        print("Delete from test where test1 = 3")
        self.sqlite.delete("test", "test1='3'")
        self.sqlite.print_all("test")

    def tearDown(self):
        self.sqlite.close_connection()
        os.remove("test.db")
        # TODO aggiungere elimina DB

if __name__ == '__main__':
    unittest.main()