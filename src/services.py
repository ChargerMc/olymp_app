from src.repos import SportsComplexRepository, OlympicVenueRepository
from src.models import SingleSportComplex, MultiSportComplex, Event, OlympicVenue, SportsComplex

class SportsComplexService:
    def __init__(self, repository: SportsComplexRepository):
        self.repository = repository

    def add_complex(self, complex):
        self.repository.add_complex(complex)

    def list_complexes(self):
        return self.repository.get_all_complexes()

    def add_event_to_complex(self, complex_name: str, event: Event):
        complex = self.repository.find_by_name(complex_name)
        if not complex:
            raise ValueError(f"Complejo '{complex_name}' no encontrado.")

        for existing_event in complex.events:
            if existing_event.date == event.date:
                raise ValueError(f"Ya existe un evento en la fecha {event.date} para el complejo '{complex_name}'.")
            
        complex.add_event(event)
        return True

class OlympicVenueService:
    def __init__(self, repository: OlympicVenueRepository):
        self.repository = repository

    def add_venue(self, venue: OlympicVenue):
        self.repository.add_venue(venue)

    def list_venues(self):
        return self.repository.get_all_venues()
    
    def add_complex_to_venue(self, venue_name: str, complex: SportsComplex, budget: float):
        venue = self.repository.find_by_name(venue_name)
        if not venue:
            raise ValueError(f"Sede '{venue_name}' no encontrada.")
        venue.add_complex(complex, budget)
        return True

    def add_event_to_complex(self, complex_name: str, event: Event):
        complex = self.repository.find_by_name(complex_name)
        if not complex:
            raise ValueError(f"Complejo '{complex_name}' no encontrado.")

        for existing_event in complex.events:
            if existing_event.date == event.date:
                raise ValueError(f"Ya existe un evento en la fecha {event.date} para el complejo '{complex_name}'.")
            
        complex.add_event(event)
        return True

    def get_venue_info(self, venue_name: str):
        venue = self.repository.find_by_name(venue_name)
        if not venue:
            raise ValueError(f"Sede '{venue_name}' no encontrada.")
        return {
            "name": venue.name,
            "num_single_sport_complexes": venue.num_single_sport_complexes,
            "num_multi_sport_complexes": venue.num_multi_sport_complexes,
            "single_sport_budget": venue.single_sport_budget,
            "multi_sport_budget": venue.multi_sport_budget,
            "complexes": [self.get_complex_info(complex) for complex in venue.complexes]
            }

    def get_complex_info(self, complex):
        info = {
            "name": complex.name,
            "location": complex.location,
            "manager": complex.manager,
            "total_area": complex.total_area,
            "events": [{"name": e.name, "date": e.date.strftime('%Y-%m-%d'), "duration": e.duration, 
                        "num_participants": e.num_participants, "num_judges": e.num_judges} for e in complex.events]
        }
        if isinstance(complex, SingleSportComplex):
            info["type"] = "Single Sport"
            info["sport"] = complex.sport
        elif isinstance(complex, MultiSportComplex):
            info["type"] = "Multi Sport"
            info["areas"] = complex.areas
        return info
