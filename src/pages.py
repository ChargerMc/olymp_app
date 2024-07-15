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
        self.venue_name_input = ft.TextField(label="Venue Name", width=300)
        self.venue_select = ft.Dropdown(label="Select Venue", width=300, options=[])
        self.complex_select = ft.Dropdown(label="Select Complex", width=300, options=[])

        # Single Sport Complex Inputs
        self.single_sport_inputs = [
            ft.TextField(label="Complex Name", width=200),
            ft.TextField(label="Location", width=200),
            ft.TextField(label="Manager", width=200),
            ft.TextField(label="Sport", width=200),
            ft.TextField(label="Total Area", width=150),
            ft.TextField(label="Budget", width=150),
        ]

        # Multi Sport Complex Inputs
        self.multi_sport_inputs = [
            ft.TextField(label="Complex Name", width=200),
            ft.TextField(label="Location", width=200),
            ft.TextField(label="Manager", width=200),
            ft.TextField(label="Total Area", width=150),
            ft.TextField(label="Budget", width=150),
        ]
        self.multi_sport_areas = ft.Column()
        self.add_area_button = ft.ElevatedButton("Add Area", on_click=self.add_area_input)

        # Event Inputs
        self.event_inputs = [
            ft.TextField(label="Event Name", width=200),
            ft.TextField(label="Date (YYYY-MM-DD)", width=150),
            ft.TextField(label="Duration (hours)", width=150),
            ft.TextField(label="Number of Participants", width=150),
            ft.TextField(label="Number of Judges", width=150),
        ]
        
    def add_area_input(self, e=None):
        area_row = ft.Row([
            ft.TextField(label="Sport", width=150),
            ft.TextField(label="Area", width=100),
            ft.TextField(label="Location", width=150),
            ft.IconButton(icon=ft.icons.DELETE, on_click=lambda _: self.remove_area_input(area_row))
        ])
        self.multi_sport_areas.controls.append(area_row)
        self.update()
        
    def remove_area_input(self, area_row):
        self.multi_sport_areas.controls.remove(area_row)
        self.update()
        
    def add_multi_sport_complex(self, e):
        if not self.venue_select.value:
            self.show_snack_bar("Please select a venue first.")
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
                raise ValueError("At least one area must be added.")
        except ValueError as ve:
            self.show_snack_bar(f"Invalid input: {str(ve)}")
            return
        
        complex = MultiSportComplex(name, location, manager, total_area, areas)
        self.complex_service.add_complex(complex)
        self.venue_service.add_complex_to_venue(self.venue_select.value, complex, budget)
        self.complex_list.controls.append(ft.Text(f"Added multi sport complex: {name}"))
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
            self.show_snack_bar("Please enter a venue name.")
            return
        venue = OlympicVenue(name)
        self.venue_service.add_venue(venue)
        self.venue_list.controls.append(ft.Text(f"Added venue: {name}"))
        self.venue_select.options.append(ft.dropdown.Option(name))
        self.venue_name_input.value = ""
        self.update()

    def add_single_sport_complex(self, e):
        if not self.venue_select.value:
            self.show_snack_bar("Please select a venue first.")
            return
        try:
            name, location, manager, sport, total_area, budget = [input.value for input in self.single_sport_inputs]
            total_area = float(total_area)
            budget = float(budget)
        except ValueError:
            self.show_snack_bar("Invalid input. Please check all fields.")
            return
        
        complex = SingleSportComplex(name, location, manager, total_area, sport)
        self.complex_service.add_complex(complex)
        self.venue_service.add_complex_to_venue(self.venue_select.value, complex, budget)
        self.complex_list.controls.append(ft.Text(f"Added single sport complex: {name}"))
        self.complex_select.options.append(ft.dropdown.Option(name))
        self.clear_inputs(self.single_sport_inputs)
        self.update()

    def add_event(self, e):
        if not self.complex_select.value:
            self.show_snack_bar("Please select a complex first.")
            return
        try:
            name, date, duration, num_participants, num_judges = [input.value for input in self.event_inputs]
            duration = int(duration)
            num_participants = int(num_participants)
            num_judges = int(num_judges)
        except ValueError:
            self.show_snack_bar("Invalid input. Please check all fields.")
            return
        
        event = Event(name, date, duration, num_participants, num_judges)
        if self.complex_service.add_event_to_complex(self.complex_select.value, event):
            self.show_snack_bar(f"Added event: {name} to complex: {self.complex_select.value}")
            self.clear_inputs(self.event_inputs)
        else:
            self.show_snack_bar("Failed to add event. Complex not found.")
        self.update()

    def show_venue_info(self, e):
        if not self.venue_select.value:
            self.show_snack_bar("Please select a venue to view info.")
            return
        info = self.venue_service.get_venue_info(self.venue_select.value)
        if info:
            self.venue_info.controls.clear()
            self.venue_info.controls.extend([
                ft.Text(f"Venue: {info['name']}", size=18, weight=ft.FontWeight.BOLD),
                ft.Text(f"Single Sport Complexes: {info['num_single_sport_complexes']}", size=14),
                ft.Text(f"Multi Sport Complexes: {info['num_multi_sport_complexes']}", size=14),
                ft.Text(f"Single Sport Budget: ${info['single_sport_budget']:,.2f}", size=14),
                ft.Text(f"Multi Sport Budget: ${info['multi_sport_budget']:,.2f}", size=14),
                ft.Divider(),
                ft.Text("Complexes:", size=16, weight=ft.FontWeight.BOLD),
            ])
            for complex in info['complexes']:
                complex_info = [
                    ft.Text(f"Name: {complex['name']}", size=14, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Type: {complex['type']}", size=14),
                    ft.Text(f"Location: {complex['location']}", size=14),
                    ft.Text(f"Manager: {complex['manager']}", size=14),
                    ft.Text(f"Total Area: {complex['total_area']} sq m", size=14),
                ]
                if complex['type'] == "Single Sport":
                    complex_info.append(ft.Text(f"Sport: {complex['sport']}", size=14))
                else:
                    areas_text = "; ".join([f"{sport}: {details['area']} sq m, {details['location']}" for sport, details in complex['areas'].items()])
                    complex_info.append(ft.Text(f"Areas: {areas_text}", size=14))
                
                if complex['events']:
                    complex_info.append(ft.Text("Events:", size=14, weight=ft.FontWeight.BOLD))
                    for event in complex['events']:
                        complex_info.append(ft.Text(
                            f"{event['name']} - Date: {event['date']}, Duration: {event['duration']} hours, "
                            f"Participants: {event['num_participants']}, Judges: {event['num_judges']}", 
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
            self.venue_info.controls.append(ft.Text(f"Venue {self.venue_select.value} not found", color=ft.colors.RED))
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
        if self.current_tab == 0:
            self.tab_content.content = ft.Column([
                ft.Row([
                    self.venue_name_input,
                    ft.ElevatedButton("Add Venue", on_click=self.add_venue)
                ]),
                ft.Text("Added Venues:", size=16, weight=ft.FontWeight.BOLD),
                self.venue_list,
            ])
        elif self.current_tab == 1:
            self.tab_content.content = ft.Column([
                self.venue_select,
                ft.Row(self.single_sport_inputs),
                ft.ElevatedButton("Add Single Sport Complex", on_click=self.add_single_sport_complex),
                ft.Text("Added Complexes:", size=16, weight=ft.FontWeight.BOLD),
                self.complex_list,
            ])
        elif self.current_tab == 2:
            self.tab_content.content = ft.Column([
                self.venue_select,
                ft.Row(self.multi_sport_inputs),
                ft.Text("Areas:", size=16, weight=ft.FontWeight.BOLD),
                self.multi_sport_areas,
                self.add_area_button,
                ft.ElevatedButton("Add Multi Sport Complex", on_click=self.add_multi_sport_complex),
                ft.Text("Added Complexes:", size=16, weight=ft.FontWeight.BOLD),
                self.complex_list,
            ])
        elif self.current_tab == 3:
            self.tab_content.content = ft.Column([
                self.complex_select,
                ft.Row(self.event_inputs),
                ft.ElevatedButton("Add Event", on_click=self.add_event),
            ])
        elif self.current_tab == 4:
            self.tab_content.content = ft.Column([
                self.venue_select,
                ft.ElevatedButton("Show Venue Info", on_click=self.show_venue_info),
                self.venue_info,
            ])

    def build(self):
        self.update_tab_content()
        return ft.Column([
            ft.Tabs(
                selected_index=self.current_tab,
                animation_duration=300,
                tabs=[
                    ft.Tab(text="Venues", icon=ft.icons.STADIUM),
                    ft.Tab(text="Single Sport Complex", icon=ft.icons.SPORTS_TENNIS),
                    ft.Tab(text="Multi Sport Complex", icon=ft.icons.SPORTS_SOCCER),
                    ft.Tab(text="Add Event", icon=ft.icons.EVENT),
                    ft.Tab(text="Venue Info", icon=ft.icons.INFO),
                ],
                on_change=self.change_tab,
            ),
            self.tab_content,
        ])