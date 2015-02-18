__author__ = 'Davide Monfrecola'

import sqlite3
import sys

class SqliteConnector():
    ''' Sqlite wrapper library '''

    def __init__(self, db):
        self.database = db
        self.conn = None
        self.cursor = None
        pass

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.database)
            self.cursor = self.conn.cursor()
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

    def create(self, sql):
        try:
            pass
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

    def insert(self, sql):
        try:
            pass
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

    def update(self, sql):
        try:
            pass
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)