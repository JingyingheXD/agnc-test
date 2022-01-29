# from datetime import datetime


# class Ticket:
#     def __init__(self, performed_at, ticket_id, performer_type, performer_id, activity):
#         self.performed_at = performed_at
#         self.ticket_id = ticket_id
#         self.performer_type = performer_type
#         self.performer_id = performer_id
#         self.activity = activity

#     def convert_time_format(self, dt_time):
#         str_time = datetime.strftime(dt_time, '%d-%m-%Y %H:%M:%S %z')
#         return str_time

#     def output_ticket(self):
#         return(
#             {
#                 'performed_at': self.convert_time_format(self.performed_at),
#                 'ticket_id': self.ticket_id,
#                 'performer_type': self.performer_type,
#                 'performer_id': self.performer_id,
#                 'activity': self.activity
#             }
#         )


class Activity:
    def __init__(self, activity_id, performed_at):
        self.activity = activity_id
        self.performed_at = performed_at
