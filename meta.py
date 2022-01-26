class Meta:
    def __init__(self, start_at, end_at, activities_count):
        self.start_at = start_at
        self.end_at = end_at
        self.activities_count = activities_count

    def output_meta(self):
        return(
            {
                'start_at': self.start_at,
                'end_at': self.end_at,
                'activities_count': self.activities_count
            }
        )
