import flet as ft

from services.events_service import EventService

events = EventService()


def main(page: ft.Page):
    page.add(ft.SafeArea(ft.Column(
        [
        ft.Text(f"Estos son los eventos actuales: {events.get_events()}"),
        ft.ElevatedButton("Crear evento", on_click=lambda: events.create_event("Evento")),
    ])))


ft.app(main)
