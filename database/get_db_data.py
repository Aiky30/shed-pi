import sqlite3

from database.constants import DB_NAME


def get_all_data():
      db = sqlite3.connect(DB_NAME)
      cursor = db.cursor()
      cursor.execute("SELECT * FROM device_reading")
      rows = cursor.fetchall()
      db.close()
      return rows


if __name__ == '__main__':
    data = get_all_data()

    for row in data:
        print(row)
