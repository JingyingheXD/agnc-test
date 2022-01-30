import json
import sqlite3


conn = sqlite3.connect('freshdesk_db.sqlite')
cur = conn.cursor()

# Create table Agents, Tickets, Activity, Act_Order, Act_Note
cur.execute('''
    CREATE TABLE IF NOT EXISTS Agents(
        agent_id INTEGER,
        agents_type CHAR(8),
        PRIMARY KEY (agent_id)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS Tickets(
        ticket_id INTEGER,
        agent_id INTEGER,
        PRIMARY KEY (ticket_id),
        FOREIGN KEY (agent_id) REFERENCES Agents (agent_id)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS Activity(
        activity_id INTEGER,
        ticket_id INTEGER,
        performed_at DATETIME,
        PRIMARY KEY (activity_id),
        FOREIGN KEY (ticket_id) REFERENCES Tickets (ticket_id) ON DELETE CASCADE
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS Act_Order(
        order_id INTEGER,
        activity_id INTEGER,
        shipping_address TEXT,
        shipment_date DATE,
        priority INTEGER,
        issue_type CHAR(20),
        order_status TEXT,
        order_group CHAR(20),
        category CHAR(20),
        order_source INTEGER,
        requester INTEGER,
        product CHAR(20),
        contacted_customer BOOLEAN,
        PRIMARY KEY (order_id),
        FOREIGN KEY (activity_id) REFERENCES Activity (activity_id) ON DELETE CASCADE
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS Act_Note(
        note_id INTEGER,
        activity_id INTEGER,
        note_type INTEGER,
        PRIMARY KEY (note_id),
        FOREIGN KEY (note_id) REFERENCES Activity (activity_id) ON DELETE CASCADE
    )
''')


# Insert JSON data into databse
all_data = json.load(open('activities.json'))
activities = all_data['activities_data']

query1 = 'INSERT OR REPLACE INTO Agents VALUES (?,?)'
query2 = 'INSERT OR REPLACE INTO Tickets VALUES (?,?)'
query3 = 'INSERT INTO Activity (agent_id, performed_at) VALUES (?,?)'
query4 = 'INSERT INTO Act_Order (activity_id,shipping_address, shipment_date,priority,issue_type,order_status,order_group,category,order_source,requester,product,contacted_customer) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'
query5 = 'INSERT INTO Act_Note VALUES (?,?,?)'

try:
    for activity in activities:
        cur.execute(
            query1, (activity['performer_id'], activity['performer_type']))
        cur.execute(query2, (activity['ticket_id'], activity['performer_id']))
        cur.execute(
            query3, (activity['performer_id'], activity['performed_at']))
        activity_id = cur.lastrowid
        if 'note' not in activity['activity'].keys():
            cur.execute(query4, (activity_id, activity['activity']['shipping_address'], activity['activity']['shipment_date'], activity['activity']['priority'], activity['activity']['issue_type'], activity['activity']['status'],
                                 activity['activity']['group'], activity['activity']['category'], activity['activity']['source'], activity['activity']['requester'], activity['activity']['product'], activity['activity']['contacted_customer']))
        else:
            cur.execute(query5, (activity['activity']['note']['id'],
                        activity_id, activity['activity']['note']['type']))
except sqlite3.IntegrityError as e:
    print('Error occurred: ', e)


cur.close()
conn.commit()
