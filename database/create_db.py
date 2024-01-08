import sqlite3

from database.constants import DB_NAME

def create_table():
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS device_reading (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_temp float NOT NULL,
            probe_temp float NOT NULL
        )
    """)
    db.commit()
    db.close()


if __name__ == '__main__':
    create_table()
