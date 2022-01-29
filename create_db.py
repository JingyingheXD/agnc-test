import sqlite3


conn = sqlite3.connect('tickets_db')
c = conn.cursor()

c.execute('''
    CREATE TABLE tickets(
        [ticket_id] INTEGER PRIMARY KEY,
        [performed_at] TEXT)
''')

cur.close()
conn.commit()
