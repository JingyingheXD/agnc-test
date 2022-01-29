class Note:
    def __init__(self, note_id, note_type):
        self.note_id = note_id
        self.note_type = note_type

    def output_note(self):
        return(
            {
                'note': {
                    'id': self.note_id,
                    'type': self.note_type
                }
            }
        )
