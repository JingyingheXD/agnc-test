import sqlite3


conn = sqlite3.connect('freshdesk_db.sqlite')
cur = conn.cursor()

cur.execute(sql)


cur.close()
conn.commit()
