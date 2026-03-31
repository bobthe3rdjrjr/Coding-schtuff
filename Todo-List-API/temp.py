import sqlite3
conn = sqlite3.connect("instance/app.db")
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(user_model)")
print(cursor.fetchall())