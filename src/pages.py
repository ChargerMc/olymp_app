import flet as ft

from src.models import OlympicVenue, SingleSportComplex, MultiSportComplex, Event
from src.repos import DataStore
from src.services import SportsComplexService, OlympicVenueService

class OlympApp(ft.UserControl):
    def __init__(self, page: ft.Page, store: DataStore):
        super().__init__()
        self.page = page
        self.complex_service = SportsComplexService(store.sports_complexes)
        self.venue_service = OlympicVenueService(store.olympic_venues)
        
        self.init_inputs()
        self.init_lists()
        self.current_tab = 0
        self.tab_content = ft.Container(padding=20)

    def init_inputs(self):
        self.venue_name_input = ft.TextField(label="Nombre de la sede", width=300)
        self.venue_select = ft.Dropdown(label="Seleccionar sede", width=300, options=[])
        self.complex_select = ft.Dropdown(label="Seleccionar complejo", width=300, options=[])

        self.single_sport_inputs = [
            ft.TextField(label="Nombre del complejo", width=200),
            ft.TextField(label="Ubicación", width=200),
            ft.TextField(label="Nombre del administrador", width=200),
            ft.TextField(label="Deporte", width=200),
            ft.TextField(label="Área totala (m2)", width=150),
            ft.TextField(label="Presupuesto", width=150),
        ]

        self.multi_sport_inputs = [
            ft.TextField(label="Nombre del complejo", width=200),
            ft.TextField(label="Ubicación", width=200),
            ft.TextField(label="Nombre del administrador", width=200),
            ft.TextField(label="Área totala (m2)", width=150),
            ft.TextField(label="Presupuesto", width=150),
        ]
        self.multi_sport_areas = ft.Column()
        self.add_area_button = ft.ElevatedButton("Añadir área", on_click=self.add_area_input)

        self.event_inputs = [
            ft.TextField(label="Nombre del evento", width=200),
            ft.TextField(label="Fecha (YYYY-MM-DD)", width=150),
            ft.TextField(label="Duración (horas)", width=150),
            ft.TextField(label="Número de participantes", width=150),
            ft.TextField(label="Número de jueces", width=150),
        ]
        
    def add_area_input(self, e=None):
        area_row = ft.Row([
            ft.TextField(label="Deporte", width=150),
            ft.TextField(label="Área (m2)", width=100),
            ft.TextField(label="Ubicación", width=150),
            ft.IconButton(icon=ft.icons.DELETE, on_click=lambda _: self.remove_area_input(area_row))
        ])
        self.multi_sport_areas.controls.append(area_row)
        self.update()
        
    def remove_area_input(self, area_row):
        self.multi_sport_areas.controls.remove(area_row)
        self.update()
        
    def add_multi_sport_complex(self, e):
        if not self.venue_select.value:
            self.show_snack_bar("Selecciona la sede primero.")
            return
        try:
            name, location, manager, total_area, budget = [input.value for input in self.multi_sport_inputs]
            total_area = float(total_area)
            budget = float(budget)
            areas = {}
            for area_row in self.multi_sport_areas.controls:
                sport = area_row.controls[0].value
                area = float(area_row.controls[1].value)
                location = area_row.controls[2].value
                areas[sport.strip()] = {"area": area, "location": location.strip()}
            if not areas:
                raise ValueError("Al menos una área debe ser añadida.")
        except ValueError as ve:
            self.show_snack_bar(f"Valor inválido: {str(ve)}")
            return
        
        complex = MultiSportComplex(name, location, manager, total_area, areas)
        self.complex_service.add_complex(complex)
        self.venue_service.add_complex_to_venue(self.venue_select.value, complex, budget)
        self.complex_list.controls.append(ft.Text(f"Añadido complejo multi deporte: {name}"))
        self.complex_select.options.append(ft.dropdown.Option(name))
        self.clear_inputs(self.multi_sport_inputs)
        self.multi_sport_areas.controls.clear()
        self.update()

    def init_lists(self):
        self.venue_list = ft.Column(scroll=ft.ScrollMode.AUTO, height=400)
        self.complex_list = ft.Column(scroll=ft.ScrollMode.AUTO, height=400)
        self.venue_info = ft.Column(scroll=ft.ScrollMode.AUTO, height=400)

    def add_venue(self, e):
        name = self.venue_name_input.value
        if not name:
            self.show_snack_bar("Ingresa el nombre de la sede.")
            return
        venue = OlympicVenue(name)
        self.venue_service.add_venue(venue)
        self.venue_list.controls.append(ft.Text(f"Sede añadida: {name}"))
        self.venue_select.options.append(ft.dropdown.Option(name))
        self.venue_name_input.value = ""
        self.update()

    def add_single_sport_complex(self, e):
        if not self.venue_select.value:
            self.show_snack_bar("Porfavor selecciona la sede primero.")
            return
        try:
            name, location, manager, sport, total_area, budget = [input.value for input in self.single_sport_inputs]
            total_area = float(total_area)
            budget = float(budget)
        except ValueError:
            self.show_snack_bar("Campo inválido, porfavor verifica todos los campos.")
            return
        
        complex = SingleSportComplex(name, location, manager, total_area, sport)
        self.complex_service.add_complex(complex)
        self.venue_service.add_complex_to_venue(self.venue_select.value, complex, budget)
        self.complex_list.controls.append(ft.Text(f"Añadido complejo de unideporte: {name}"))
        self.complex_select.options.append(ft.dropdown.Option(name))
        self.clear_inputs(self.single_sport_inputs)
        self.update()

    def add_event(self, e):
        if not self.complex_select.value:
            self.show_snack_bar("Porfavor selecciona el complejo primero.")
            return
        try:
            name, date, duration, num_participants, num_judges = [input.value for input in self.event_inputs]
            duration = int(duration)
            num_participants = int(num_participants)
            num_judges = int(num_judges)
        except ValueError:
            self.show_snack_bar("Campo inválido. Porfavor verifica todos los campos.")
            return
        
        event = Event(name, date, duration, num_participants, num_judges)
        if self.complex_service.add_event_to_complex(self.complex_select.value, event):
            self.show_snack_bar(f"Evento añadido: {name} al complejo: {self.complex_select.value}")
            self.clear_inputs(self.event_inputs)
        else:
            self.show_snack_bar("Ocurrió un error al crear el evento. Complejo no encontrado.")
        self.update()

    def show_venue_info(self, e):
        if not self.venue_select.value:
            self.show_snack_bar("Porfavor selecciona la sede para ver la información.")
            return
        info = self.venue_service.get_venue_info(self.venue_select.value)
        if info:
            self.venue_info.controls.clear()
            self.venue_info.controls.extend([
                ft.Text(f"Sede: {info['name']}", size=18, weight=ft.FontWeight.BOLD),
                ft.Text(f"Complejos unideporte: {info['num_single_sport_complexes']}", size=14),
                ft.Text(f"Complejos multi deporte: {info['num_multi_sport_complexes']}", size=14),
                ft.Text(f"Presupuesto unideporte: ${info['single_sport_budget']:,.2f}", size=14),
                ft.Text(f"Presupuesto multi deporte: ${info['multi_sport_budget']:,.2f}", size=14),
                ft.Divider(),
                ft.Text("Complejos:", size=16, weight=ft.FontWeight.BOLD),
            ])
            for complex in info['complexes']:
                complex_info = [
                    ft.Text(f"Nombre: {complex['name']}", size=14, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Tipo: {complex['type']}", size=14),
                    ft.Text(f"Ubicación: {complex['location']}", size=14),
                    ft.Text(f"Administrador: {complex['manager']}", size=14),
                    ft.Text(f"Área total (m2): {complex['total_area']} sq m", size=14),
                ]
                if complex['type'] == "Single Sport":
                    complex_info.append(ft.Text(f"Sport: {complex['sport']}", size=14))
                else:
                    areas_text = "; ".join([f"{sport}: {details['area']} m2, {details['location']}" for sport, details in complex['areas'].items()])
                    complex_info.append(ft.Text(f"Áreas: {areas_text}", size=14))
                
                if complex['events']:
                    complex_info.append(ft.Text("Eventos:", size=14, weight=ft.FontWeight.BOLD))
                    for event in complex['events']:
                        complex_info.append(ft.Text(
                            f"{event['name']} - Fecha: {event['date']}, Duración: {event['duration']} horas, "
                            f"Participantes: {event['num_participants']}, Jueces: {event['num_judges']}", 
                            size=12
                        ))
                
                self.venue_info.controls.append(
                    ft.Container(
                        content=ft.Column(complex_info),
                        padding=10,
                        border=ft.border.all(1, ft.colors.GREY_400),
                        border_radius=5,
                        margin=5,
                    )
                )
        else:
            self.venue_info.controls.append(ft.Text(f"Sede {self.venue_select.value} no encontrada", color=ft.colors.RED))
        self.update()

    def show_snack_bar(self, text):
        self.page.snack_bar = ft.SnackBar(ft.Text(text))
        self.page.snack_bar.open = True
        self.page.update()

    def clear_inputs(self, inputs):
        for input_field in inputs:
            input_field.value = ""

    def change_tab(self, e):
        self.current_tab = e.control.selected_index
        self.update_tab_content()
        self.update()

    def update_tab_content(self):
        match self.current_tab:
            case 0:
                self.tab_content.content = ft.Column([
                    ft.Row([
                        self.venue_name_input,
                        ft.ElevatedButton("Añadir sede", on_click=self.add_venue)
                    ]),
                    ft.Text("Sedes añadidas:", size=16, weight=ft.FontWeight.BOLD),
                    self.venue_list,
            ])
            case 1:
                self.tab_content.content = ft.Column([
                    self.venue_select,
                    ft.Row(self.single_sport_inputs),
                    ft.ElevatedButton("Añadir complejo unideporte", on_click=self.add_single_sport_complex),
                    ft.Text("Complejos añadidos:", size=16, weight=ft.FontWeight.BOLD),
                    self.complex_list,
            ])
            case 2:
                self.tab_content.content = ft.Column([
                    self.venue_select,
                    ft.Row(self.multi_sport_inputs),
                    ft.Text("Áreas:", size=16, weight=ft.FontWeight.BOLD),
                    self.multi_sport_areas,
                    self.add_area_button,
                    ft.ElevatedButton("Aladir complejo multideporte", on_click=self.add_multi_sport_complex),
                    ft.Text("Complejos añadidos:", size=16, weight=ft.FontWeight.BOLD),
                    self.complex_list,
            ])
            case 3:
                self.tab_content.content = ft.Column([
                    self.complex_select,
                    ft.Row(self.event_inputs),
                    ft.ElevatedButton("Añadir evento", on_click=self.add_event),
            ])
            case 4:
                self.tab_content.content = ft.Column([
                    self.venue_select,
                    ft.ElevatedButton("Mostrar información de la sede", on_click=self.show_venue_info),
                    self.venue_info,
            ])

    def build(self):
        self.update_tab_content()
        return ft.Column([
            ft.Tabs(
                selected_index=self.current_tab,
                animation_duration=300,
                tabs=[
                    ft.Tab(text="Sedes", icon=ft.icons.STADIUM),
                    ft.Tab(text="Complejo unideporte", icon=ft.icons.SPORTS_TENNIS),
                    ft.Tab(text="Complejo multideporte", icon=ft.icons.SPORTS_SOCCER),
                    ft.Tab(text="Añadir evento", icon=ft.icons.EVENT),
                    ft.Tab(text="Información de la sede", icon=ft.icons.INFO),
                ],
                on_change=self.change_tab,
            ),
            self.tab_content,
        ])