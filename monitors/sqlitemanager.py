__author__ = 'Davide Monfrecola'

import sqlite3
import sys


class SqliteConnector():
    ''' Sqlite wrapper library '''

    def __init__(self, db):
        self.database = db
        self.conn = None
        self.cursor = None

    def connect(self):
        #print("Connecting to database %s" % self.database)
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()

    def close_connection(self):
        self.conn.close()

    def create(self, table, columns):
        sql = "CREATE TABLE {0} ({1})".format(table, columns)
        self.query_and_commit(sql)

    def insert(self, table, values):
        sql = "INSERT INTO %s VALUES (%s)" % (table, values)
        self.query_and_commit(sql)

    def update(self, table, set, where='1'):
        sql = "UPDATE %s SET %s WHERE %s" % (table, set, where)
        self.query_and_commit(sql)

    def delete(self, table, where='1'):
        sql = "DELETE FROM %s WHERE %s" % (table, where)
        self.query_and_commit(sql)

    def query_and_commit(self, sql):
        try:
            self.connect()
            self.cursor.execute(sql)

            self.conn.commit()
            self.close_connection()
        except sqlite3.Error, e:
            # TODO gestire con log, eliminare sys.exit(1)
            print "Error %s:" % e.args[0]
            sys.exit(1)

    def query(self, sql):
        try:
            self.connect()

            rows = self.cursor.execute(sql)

            return rows
        except sqlite3.Error, e:
            # TODO gestire con log, eliminare sys.exit(1)
            print "Error %s:" % e.args[0]
            sys.exit(1)

    def print_all(self, table):
        rows = self.query("SELECT * FROM %s" % table)

        for row in rows:
            print row

        self.close_connection()

    def delete_all(self, table):
        self.query("DELETE FROM %s" % table)