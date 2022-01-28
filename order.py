class Order:
    def _init_(self, performed_at, shipping_address, shipment_date, priority, activity_type, status, group, category, source, requester, product, contacted_customer):
        self.performed_at = performed_at
        self.shipping_address = shipping_address
        self.shipment_date = shipment_date
        self.priority = priority
        self.activity_type = activity_type
        self.status = status
        self.group = group
        self.category = category
        self.source = source
        self.requester = requester
        self.product = product
        self.contacted_customer = contacted_customer
