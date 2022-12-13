import sqlite3
import json


class Database:
    def __init__(self, database_path, schema_path):
        self.connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        self.init_db(schema_path)

    def init_db(self, schema_path):
        with open(schema_path, mode="r") as schema:
            self.cursor.executescript(schema.read())

        self.connection.commit()

    def get_events(self, json=True):
        events = self.query_db("SELECT * FROM party_event")

        if json:
            events = [dict(event) for event in events]

        return events

    def add_event(self, name, is_approved):
        new_event = self.insert_into_db("INSERT INTO party_event(name,is_approved) VALUES(?,?)", [
            name, is_approved])

        return new_event

    def query_db(self, query, args=(), one=False):
        results = self.cursor.execute(query, args)
        rows = results.fetchall()

        return (rows[0] if rows else None) if one else rows

    def insert_into_db(self, query, args=()):
        row = self.cursor.execute(query, args)

        self.connection.commit()

        return row

    def close(self):
        self.cursor.close()
