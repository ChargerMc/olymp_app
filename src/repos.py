from src.models import SportsComplex, OlympicVenue
from typing import List

class SportsComplexRepository:
    def __init__(self):
        self.complexes: List[SportsComplex] = []

    def add_complex(self, complex: SportsComplex):
        self.complexes.append(complex)
        
    def remove_complex(self, complex: SportsComplex):
        self.complexes.remove(complex)

    def get_all_complexes(self):
        return self.complexes
    
    def find_by_name(self, name):
        for complex in self.complexes:
            if complex.name == name:
                return complex
        return None

class OlympicVenueRepository:
    def __init__(self):
        self.venues: List[OlympicVenue] = []

    def add_venue(self, venue: OlympicVenue):
        self.venues.append(venue)
        
    def remove_venue(self, venue: OlympicVenue):
        self.venues.remove(venue)

    def get_all_venues(self):
        return self.venues

    def find_by_name(self, name):
        for venue in self.venues:
            if venue.name == name:
                return venue
        return None

class DataStore:
    def __init__(self):
        self.sports_complexes = SportsComplexRepository()
        self.olympic_venues = OlympicVenueRepository()