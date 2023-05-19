import traceback
import sqlite3
from scripts.logging import logger_util

LOG = logger_util.get_logger()


class SQLiteDBUtility(object):
    def __init__(self):
        ""

    def execute(self, db, query):
        try:
            __sqlite_obj__ = sqlite3.connect(db)
            cursor = __sqlite_obj__.execute(query)
            return cursor
        except Exception as error:
            traceback.print_exc()
            raise Exception(str(error))

    def row_to_dict(self, cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict:
        data = {}
        for idx, col in enumerate(cursor.description):
            data[col[0]] = row[idx]
        return data

    def fetch_all(self, db, query):
        with sqlite3.connect(db) as con:
            con.row_factory = self.row_to_dict
            result = con.execute(query)
            return result.fetchall()
