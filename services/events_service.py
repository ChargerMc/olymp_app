from models.events import Event

class EventService:
    def __init__(self):
        self.event_repository = {};

    def create_event(self, event: Event):
        return self.event_repository.append(event)

    def get_event(self, event_id):
        return self.event_repository.get(event_id)

    def get_events(self):
        return self.event_repository

    def update_event(self, event_id, event: Event):        
        return self.event_repository.update_event(event_id, event)

    def delete_event(self, event_id):
        return self.event_repository.delete_event(event_id)