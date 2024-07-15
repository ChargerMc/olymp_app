from datetime import datetime
from typing import List, Dict

class Event:
    def __init__(self, name: str, date: str, duration: int, num_participants: int, num_judges: int):
        self.name = name
        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.duration = duration
        self.num_participants = num_participants
        self.num_judges = num_judges

class SportsComplex:
    def __init__(self, name: str, location: str, manager: str, total_area: float):
        self.name = name
        self.location = location
        self.manager = manager
        self.total_area = total_area
        self.events: List[Event] = []

    def add_event(self, event: Event):
        self.events.append(event)
        
    def remove_event(self, event: Event):
        self.events.remove(event)

class SingleSportComplex(SportsComplex):
    def __init__(self, name: str, location: str, manager: str, total_area: float, sport: str):
        super().__init__(name, location, manager, total_area)
        self.sport = sport

class MultiSportComplex(SportsComplex):
    def __init__(self, name: str, location: str, manager: str, total_area: float, areas: Dict[str, Dict[str, float]]):
        super().__init__(name, location, manager, total_area)
        self.areas = areas  # Format: {"Sport": {"area": float, "location": str}}

class OlympicVenue:
    def __init__(self, name: str):
        self.name = name
        self.complexes: List[SportsComplex] = []
        self.num_single_sport_complexes = 0
        self.num_multi_sport_complexes = 0
        self.single_sport_budget = 0.0
        self.multi_sport_budget = 0.0

    def add_complex(self, complex: SportsComplex, budget: float):
        self.complexes.append(complex)
        if isinstance(complex, SingleSportComplex):
            self.num_single_sport_complexes += 1
            self.single_sport_budget += budget
        elif isinstance(complex, MultiSportComplex):
            self.num_multi_sport_complexes += 1
            self.multi_sport_budget += budget

    def remove_complex(self, complex: SportsComplex):
        self.complexes.remove(complex)
        if isinstance(complex, SingleSportComplex):
            self.num_single_sport_complexes -= 1
        elif isinstance(complex, MultiSportComplex):
            self.num_multi_sport_complexes -= 1