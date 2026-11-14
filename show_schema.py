import sqlite3
conn = sqlite3.connect("data/pronunciation.db")
for (sql,) in conn.execute("SELECT sql FROM sqlite_master WHERE sql IS NOT NULL"):
    print(sql, "\n")
