import flet as ft
from src.pages import OlympApp
from src.repos import DataStore

def main(page: ft.Page):
    page.title = "Administrador de Sedes Olimpicas"
    app = OlympApp(page, DataStore())
    page.add(app)

ft.app(main)
