

import sqlite3

if __name__ == "__main__":
    db = sqlite3.connect('database/database.db')
    cursor = db.cursor()
    values = (12.2, 14)
    cursor.execute("INSERT INTO device_reading (device_temp, probe_temp) VALUES (:device_temp, :probe_temp)", values)
    db.commit()
    db.close()
