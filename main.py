# Import necessary modules
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy_garden.mapview import MapMarkerPopup, MapView
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from plyer import gps


# Define the main app class
class MyApp(MDApp):
    def build(self):
        # Create the screen manager
        self.sm = ScreenManager()

        # Create the screens
        login_screen = LoginScreen(name='login')
        map_screen = MapScreen(name='map')

        # Add screens to the screen manager
        self.sm.add_widget(login_screen)
        self.sm.add_widget(map_screen)

        return self.sm


# Define the login screen class
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        # Create a button for login
        login_button = MDRaisedButton(text="Login", pos_hint={'center_x': 0.5, 'center_y': 0.5})
        login_button.bind(on_release=self.switch_to_map)
        self.add_widget(login_button)

    def switch_to_map(self, instance):
        self.manager.current = 'map'


# Define the map screen class
class MapScreen(Screen):
    def __init__(self, **kwargs):
        super(MapScreen, self).__init__(**kwargs)

        # Create a FloatLayout
        self.float_layout = FloatLayout()

        # Create a map view
        self.map_view = MapView(zoom=12, lat=37.7749, lon=-122.4194, size_hint=(1, 1),
                                pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.float_layout.add_widget(self.map_view)

        # Create an MD card at the bottom of the screen
        card = MDCard(orientation='vertical', size_hint=(None, None), size=(600, 290),
                      pos_hint={'center_x': 0.5, 'y': 0.04}, padding=(10, 10))
        card.add_widget(MDRaisedButton(text="Some Action", size_hint=(1, None), height=40))
        self.float_layout.add_widget(card)

        # Create a card for the hamburger button
        menu_card = MDCard(size_hint=(None, None), size=(80, 80), pos_hint={'x': 0.02, 'top': 0.98})
        menu_button = MDIconButton(icon='menu', size_hint=(None, None), size=(40, 40))
        menu_card.add_widget(menu_button)
        self.float_layout.add_widget(menu_card)

        # Create a card for the GPS target button
        self.gps_card = MDCard(size_hint=(None, None), size=(80, 80), pos_hint={'x': 0.02, 'y': 0.4})
        gps_button = MDIconButton(icon='crosshairs-gps', size_hint=(None, None), size=(40, 40))
        gps_button.bind(on_release=self.locate_current_location)
        self.gps_card.add_widget(gps_button)
        self.float_layout.add_widget(self.gps_card)

        self.add_widget(self.float_layout)

    def locate_current_location(self, instance):
        gps.configure(on_location=self.on_location)
        gps.start(minTime=1000, minDistance=0)

    def on_location(self, **kwargs):
        latitude = kwargs['lat']
        longitude = kwargs['lon']
        self.map_view.center_on(latitude, longitude)


# Run the app
if __name__ == '__main__':
    MyApp().run()
