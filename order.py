from datetime import datetime

class Order:
    def __init__(self, order_id, shipping_address, shipment_date, priority, issue_type, status, group, category, source, requester, product, contacted_customer, agent_id):
        self.order_id = order_id
        self.shipping_address = shipping_address
        self.shipment_date = shipment_date
        self.priority = priority
        self.issue_type = issue_type
        self.status = status
        self.group = group
        self.category = category
        self.source = source
        self.requester = requester
        self.product = product
        self.contacted_customer = contacted_customer
        self.agent_id = agent_id

    def convert_time(self, dt_time):
        new_time = datetime.strftime(dt_time, '%d %b %Y')
        return new_time

    def output_order(self):
        return(
            {
                'shipping_address': self.shipping_address,
                'shipment_date': self.convert_time(self.shipment_date),
                'category': self.category,
                'contacted_customer': self.contacted_customer,
                'issue_type': self.issue_type,
                'source': self.source,
                'status': self.status,
                'priority': self.priority,
                'group': self.group,
                'agent_id': self.agent_id,
                'requester': self.requester,
                'product': self.product
            })
