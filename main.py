import flet as ft

from services.events_service import EventService

events = EventService()


def main(page: ft.Page):
    page.add(ft.SafeArea(ft.Text(f"Estos son los eventos actuales: {events.get_events()}")))


ft.app(main)
