import random
from faker import Faker
from datetime import datetime

from ticket import Ticket
from meta import Meta


fake = Faker()


class Mock:
    def __init__(self, activities_count=5):
        self.activities_count = activities_count
        # TODO: tickets_id increase
        self.tickets_id = set()
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

#   TODO: convert time format???+0000
    def convert_time_format(self, dt_time):
        # TODO +0000
        str_time = datetime.strftime(dt_time, '%d-%m-%Y %H:%M:%S +%z')
        return str_time

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

    def mock_activity_detail(self, start_time, performer_id):
        shipping_address = random.choice(['N/A', fake.address()])
        # TODO: how to set the end_date
        shipment_datetime = fake.date_between(
            start_date='-1y')
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
        start_at = fake.date_time_this_decade()
        # start_at = self.convert_time_format(start_at_datetime)
        end_at = fake.date_time_between_dates(
            datetime_start=start_at)
        # end_at = self.convert_time_format(end_at_datetime)
        activities_count = self.activities_count

        meta = Meta(start_at, end_at, activities_count)
        # return meta.output_meta()
        return meta

    def mock_ticket(self, start_time, end_time):
        performed_at = fake.date_time_between_dates(
            datetime_start=start_time, datetime_end=end_time)
        ticket_id = self.gen_num(self.tickets_id, 99999)
        # TODO: how to random performer?
        performer = ['user', 'admin']
        performer_type = random.choice(performer)
        performer_id = random.choice(self.performers[performer_type])

        activity = self.mock_activity_note() if random.choice(
            ['note', 'detail']) == 'note' else self.mock_activity_detail(start_time, performer_id)

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
        print(
            {
                'metadata': meta_data,
                'activities_data': activities_data
            }
        )


if __name__ == '__main__':
    data = Mock(10)
    data.combine_data()
