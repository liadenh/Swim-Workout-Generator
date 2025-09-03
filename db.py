#CREATING A DATABASE FOR SWIMMER TIMES

import sqlite3

conn = sqlite3.connect("swim.db")

c = conn.cursor()

c.execute("""
          CREATE TABLE swim_times (
          firstName TEXT NOT NULL,
          lastName TEXT NOT NULL,
          event TEXT NOT NULL,
          time TEXT NOT NULL
          )""")

conn.commit()
conn.close()

if __name__ == "__main__":
    init_db()