class Meta:
    def __init__(self, start_at, end_at, activities_count):
        self.start_at = None
        self.end_at = None
        self.activities_count = None

    def output_meta(self):
        return(
            {
                'start_at': self.start_at,
                'end_at': self.end_at,
                'activities_count': self.activities_count
            }
        )
