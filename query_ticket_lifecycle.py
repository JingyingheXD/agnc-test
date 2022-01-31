import sqlite3


conn = sqlite3.connect('freshdesk_db.sqlite')
cur = conn.cursor()

cur.execute('''
WITH 
	Ticket_Lifecycle AS(
			SELECT activity_id, ticket_id, performed_at,
			LEAD (performed_at) OVER (
				PARTITION BY ticket_id ORDER BY performed_at
			)  next_performed_at,
			(	
				julianday(
						lead(performed_at) OVER (
							PARTITION BY ticket_id ORDER BY performed_at))
			  - julianday(
						performed_at)
			) * 24 * 60  time_spent_open,
			(
				julianday(
					lead(performed_at, 2) OVER (
						PARTITION BY ticket_id ORDER BY performed_at)) 
			  - julianday(lead(performed_at) OVER (PARTITION BY ticket_id ORDER BY performed_at))
			) * 24 * 60  time_spent_waiting_on_customer,
			(
				julianday(
					lead(performed_at, 3) OVER (
						PARTITION BY ticket_id ORDER BY performed_at)) 
			 - julianday(lead(performed_at, 2) OVER (PARTITION BY ticket_id ORDER BY performed_at))
			) * 24 * 60 time_spent_waiting_for_response,
			(
				julianday(
					lead(performed_at, 4) OVER (
						PARTITION BY ticket_id ORDER BY performed_at)) 
			 - julianday(lead(performed_at, 3) OVER (PARTITION BY ticket_id ORDER BY performed_at))
			) * 24 * 60  time_till_resolution,
			(
				julianday(
					lead(performed_at, 2) OVER (
						PARTITION BY ticket_id ORDER BY performed_at)) 
			 - julianday(performed_at)
			) * 24 * 60  time_to_first_response,
			row_number() over (PARTITION BY ticket_id ORDER BY performed_at) AS rn
			FROM (
				SELECT * FROM Activity INNER JOIN Act_Order ON
				Activity.activity_id = Act_Order.activity_id)
		)
SELECT ticket_id, CAST(time_spent_open AS INT), CAST(time_spent_waiting_on_customer AS INT), CAST(time_spent_waiting_for_response AS INT), 
    CAST(time_till_resolution AS INT), CAST(time_to_first_response AS INT)
FROM Ticket_Lifecycle 
where rn = 1;
    );
''')

cur.close()
conn.commit()
