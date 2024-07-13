from models.events import Evento

class EventoLogic:
    def __init__(self, event_repository):
        self.event_repository = event_repository

    def create_event(self, event: Evento):
        return self.event_repository.create_event(event)

    def get_event(self, event_id):
        return self.event_repository.get_event(event_id)

    def get_events(self):
        return self.event_repository.get_events()

    def update_event(self, event_id, event: Evento):        
        return self.event_repository.update_event(event_id, event)

    def delete_event(self, event_id):
        return self.event_repository.delete_event(event_id)