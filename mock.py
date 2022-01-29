import random
from faker import Faker
from datetime import datetime, timezone, timedelta

from ticket import Ticket
from meta import Meta
from note import Note
from order import Order
from activity import Activity
from ticket import Ticket
from agent import Agent


fake = Faker()


class Mock:
    def __init__(self, tickets_num):
        self.tickets_num = tickets_num
        self.source_categories = {
            1: "Email",
            2: "Portal",
            3: "Phone",
            4: "Forums",
            5: "Twitter",
            6: "Facebook",
            7: "Chat",
            8: "Mobihelp",
            9: "Feedback widget",
            10: "Outbound email",
            11: "E-commerce",
            12: "Bot"
        }
        self.issue_types = ['Incident', 'Question',
                            'Problem', 'Feature Request', 'Refund']
        self.statuses = ['Open', 'Closed', 'Resolved',
                         'Waiting for Customer', 'Waiting for Third Party', 'Pending']
        self.groups = ['Refund', 'Customer Support', 'Escalations']
        self.contacted_customers = [True, False]
        self.requesters = random.sample(range(100000, 999999), 100)
        self.products = ['mobile', 'PC']
        self.tickets_id = sorted(random.sample(
            range(100, 999999), tickets_num))
        self.activity_id = fake.random_int(min=1001, max=9999)
        self.agents = {
            'user': random.sample(range(100001, 150000), 5),
            'system': 999999
        }
        self.note_id = fake.random_int(min=1000001, max=9999999)
        self.order_id = fake.random_int(min=100001, max=999999)
        self.tickets_first_performed_time = {}

    def gen_num(self, nums_set, max_num):
        # generate a non-duplicate random number (range: 1 - max_num) and store in nums_set
        while True:
            num = fake.random_int(min=1, max=max_num)
            if num not in nums_set:
                nums_set.add(num)
                return num

    def mock_agent(self):
        agent_type = random.choice(list(self.agents.keys()))
        if agent_type == 'user':
            agent_id = random.choice(self.agents['user'])
        else:
            agent_id = self.agents[agent_type]
        agent = Agent(agent_id, agent_type)
        return agent_id, agent_type

    def mock_activity_note(self):
        self.note_id += 1
        note_id = self.note_id
        note_type = fake.random_int(min=1, max=6)
        note = Note(note_id, note_type)
        return note

    def mock_activity_order(self, performed_at, performer_id):
        self.order_id += 1
        order_id = self.order_id
        shipping_address = random.choice(['N/A', fake.address()])
        shipment_datetime = fake.date_time_between(
            start_date=performed_at, end_date=performed_at+timedelta(days=180), tzinfo=timezone.utc)
        source = random.choice(list(self.source_categories.keys()))
        category = self.source_categories[source]
        priority = fake.random_int(min=1, max=4)
        issue_type = random.choice(self.issue_types)
        status = random.choice(self.statuses)
        group = random.choice(self.groups)
        contacted_customer = random.choice(self.contacted_customers)
        requester = random.choice(self.requesters)
        product = random.choice(self.products)
        agent_id = performer_id

        order = Order(order_id, shipping_address, shipment_datetime, priority, issue_type,
                      status, group, category, source, requester, product, contacted_customer, agent_id)
        return order

    def mock_activity(self, performed_at, ticket_id):
        self.activity_id += 1
        activity_id = self.activity_id
        activity = Activity(activity_id, performed_at)
        new_performed_at = datetime.strftime(
            performed_at, '%d-%m-%Y %H:%M:%S %z')
        performer_id, performer_type = self.mock_agent()

        activity_type = random.choice([0, 1])
        activity_data = None
        if activity_type == 0:
            activity_data = self.mock_activity_note().output_note()
        else:
            activity_data = self.mock_activity_order(
                performed_at, performer_id).output_order()

        return(
            {
                'performed_at': new_performed_at,
                'ticket_id': ticket_id,
                'performer_type': performer_type,
                'performer_id': performer_id,
                'activity': activity_data
            }
        )

    def mock_activities(self, start_time, end_time):
        twice_tickets_id = random.sample(
            list(self.tickets_id), self.tickets_num//2)
        activities_data = []
        st_time = start_time
        for ticket_id in self.tickets_id:
            ticket = Ticket(ticket_id)
            performed_at = fake.date_time_between_dates(
                datetime_start=st_time, datetime_end=end_time, tzinfo=timezone.utc)
            st_time = performed_at
            self.tickets_first_performed_time[ticket_id] = performed_at
            activity = self.mock_activity(performed_at, ticket_id)
            activities_data.append(activity)
        for ticket_id in twice_tickets_id:
            ticket = Ticket(ticket_id)
            performed_at = fake.date_time_between_dates(
                datetime_start=self.tickets_first_performed_time[ticket_id], datetime_end=end_time, tzinfo=timezone.utc)
            activity = self.mock_activity(performed_at, ticket_id)
            activities_data.append(activity)
        return activities_data

    def mock_meta(self):
        start_at = fake.date_time_this_decade(tzinfo=timezone.utc)
        end_at = start_at + timedelta(days=180) + timedelta(seconds=-1)
        activities_count = 0
        meta = Meta(start_at, end_at, activities_count)
        return meta

    def generate_data(self):
        meta = self.mock_meta()
        activities_data = self.mock_activities(meta.start_at, meta.end_at)
        meta.activities_count = len(activities_data)
        metadata = meta.output_meta()

        return(
            {
                'meta': metadata,
                'activities_data': activities_data
            }
        )
