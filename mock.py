import random
from faker import Faker
from datetime import datetime, timezone, timedelta

from ticket import Ticket
from meta import Meta


fake = Faker()


class Mock:
    def __init__(self, activities_count=5):
        self.activities_count = activities_count
        self.ticket_id = fake.random_int(min=101, max=999)
        self.notes_id = set()
        self.requester = set()
        self.performers = {
            'admin': [random.randrange(100000, 110000, 1) for i in range(5)],
            'user': [random.randrange(110001, 999999, 1) for i in range(100)]
        }
        self.cate = ['mobile', 'Phone', 'PC']
        self.issue_type = ['Incident', 'Change', 'Problem']
        self.status = ['Open', 'Closed', 'Resolved',
                       'Waiting for Customer', 'Waiting for Third Party', 'Pending']
        self.group = ['Normal', 'Refund']
        self.requester = [random.randrange(
            100000, 999999, 1) for i in range(100)]

    def gen_num(self, nums_set, max_num):
        # generate a non-duplicate random number
        while True:
            num = fake.random_int(min=1, max=max_num)
            if num not in nums_set:
                nums_set.add(num)
                return num

    def mock_activity_note(self):
        note_id = self.gen_num(self.notes_id, 999999)
        note_type = fake.random_int(min=1, max=20)

        note_dic = {
            'note': {
                'id': note_id,
                'type': note_type
            }
        }
        return note_dic

    def mock_activity_detail(self, performed_at, performer_id):
        shipping_address = random.choice(['N/A', fake.address()])
        shipment_datetime = fake.date_time_between(
            start_date=performed_at, end_date=performed_at+timedelta(days=180), tzinfo=timezone.utc)
        shipment_date = datetime.strftime(shipment_datetime, '%d %b %Y')
        category = random.choice(self.cate)
        contacted_customer = True
        issue_type = random.choice(self.issue_type)
        source = fake.random_int(min=1, max=10)
        status = random.choice(self.status)
        priority = fake.random_int(min=1, max=5)
        group = random.choice(self.group)
        agent_id = performer_id
        requester = random.choice(self.requester)
        product = random.choice(self.cate)

        detail_dic = {
            'shipping_address': shipping_address,
            'shipment_date': shipment_date,
            'category': category,
            'contacted_customer': contacted_customer,
            'issue_type': issue_type,
            'source': source,
            'status': status,
            'priority': priority,
            'group': group,
            'agent_id': agent_id,
            'requester': requester,
            'product': product
        }
        return detail_dic

    def mock_meta(self):
        start_at = fake.date_time_this_decade(tzinfo=timezone.utc)
        end_at = fake.date_time_between_dates(
            datetime_start=start_at, tzinfo=timezone.utc)
        activities_count = self.activities_count

        meta = Meta(start_at, end_at, activities_count)
        return meta

    def mock_ticket(self, start_time, end_time):
        performed_at = fake.date_time_between_dates(
            datetime_start=start_time, datetime_end=end_time, tzinfo=timezone.utc)
        self.ticket_id += 1
        ticket_id = self.ticket_id
        performer_type = random.choice(list(self.performers.keys()))
        performer_id = random.choice(self.performers[performer_type])

        activity = self.mock_activity_note() if random.choice(
            ['note', 'detail']) == 'note' else self.mock_activity_detail(performed_at, performer_id)

        ticket = Ticket(performed_at, ticket_id,
                        performer_type, performer_id, activity)
        return ticket

    def mock_tickets(self, start_time, end_time):
        activities_data = []
        st_time = start_time
        for _ in range(self.activities_count):
            ticket = self.mock_ticket(st_time, end_time)
            activities_data.append(ticket.output_ticket())
            st_time = ticket.performed_at
        return activities_data

    def combine_data(self):
        meta = self.mock_meta()
        meta_data = meta.output_meta()
        activities_data = self.mock_tickets(
            meta.start_at, meta.end_at)
        dic = {
            'metadata': meta_data,
            'activities_data': activities_data
        }
        print(dic)
        return dic
