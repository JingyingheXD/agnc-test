from datetime import datetime


class Meta:
    def __init__(self, start_at, end_at, activities_count):
        self.start_at = start_at
        self.end_at = end_at
        self.activities_count = activities_count

    def convert_time(self, dt_time):
        new_time = datetime.strftime(dt_time, '%d-%m-%Y %H:%M:%S %z')
        return new_time

    def output_meta(self):
        return(
            {
                'start_at': self.convert_time(self.start_at),
                'end_at': self.convert_time(self.end_at),
                'activities_count': self.activities_count
            }
        )
