class Ticket:
    def __init__(self, performed_at, ticket_id, performer_type, performer_id, activity):
        self.performed_at = None
        self.ticket_id = None
        self.performer_type = None
        self.performer_id = None
        self.activity = activity

    def output_ticket(self):
        return(
            {
                'performed_at': self.performed_at,
                'ticket_id': self.ticket_id,
                'performer_type': self.performer_type,
                'performer_id': self.performer_id,
                'activity': self.activity
            }
        )
