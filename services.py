from repos import SportsComplexRepository, OlympicVenueRepository
from models import SingleSportComplex, MultiSportComplex

class SportsComplexService:
    def __init__(self, repository: SportsComplexRepository):
        self.repository = repository

    def add_complex(self, complex):
        self.repository.add_complex(complex)

    def list_complexes(self):
        return self.repository.get_all_complexes()

class OlympicVenueService:
    def __init__(self, repository: OlympicVenueRepository):
        self.repository = repository

    def add_venue(self, venue):
        self.repository.add_venue(venue)

    def list_venues(self):
        return self.repository.get_all_venues()

    def add_complex_to_venue(self, venue_name: str, complex, budget: float):
        venue = self.repository.find_by_name(venue_name)
        if venue:
            venue.complexes.append(complex)
            if isinstance(complex, SingleSportComplex):
                venue.num_single_sport_complexes += 1
                venue.single_sport_budget += budget
            elif isinstance(complex, MultiSportComplex):
                venue.num_multi_sport_complexes += 1
                venue.multi_sport_budget += budget
            return True
        return False

    def get_venue_info(self, venue_name: str):
        venue = self.repository.find_by_name(venue_name)
        if venue:
            return {
                "name": venue.name,
                "num_single_sport_complexes": venue.num_single_sport_complexes,
                "num_multi_sport_complexes": venue.num_multi_sport_complexes,
                "single_sport_budget": venue.single_sport_budget,
                "multi_sport_budget": venue.multi_sport_budget,
                "complexes": [vars(complex) for complex in venue.complexes]
            }
        return None
