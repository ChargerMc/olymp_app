import datetime

class Event:
    def __init__(self, name: str, date: datetime, duration: int, num_participants: int, num_judges: int):
        self.name = name
        self.date = date
        self.duration = duration
        self.num_participants = num_participants
        self.num_judges = num_judges