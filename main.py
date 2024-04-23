# Import necessary modules
from kivy import utils
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy_garden.mapview import MapMarkerPopup, MapView
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from plyer import gps

if utils.platform != 'android':
    Window.size = (412, 732)


# Define the main app class
class MainApp(MDApp):
    latitude = StringProperty("37.7749")
    longitude = StringProperty("122.4194")

    def on_start(self):
        if utils.platform == 'android':
            self.request_android_permissions()

    def locate_current_location(self):
        gps.configure(on_location=self.on_location)
        gps.start(minTime=1000, minDistance=0)

    def on_location(self, **kwargs):
        self.latitude = str(kwargs['lat'])
        self.longitude = str(kwargs['lon'])

    def request_android_permissions(self):
        from android.permissions import request_permissions, Permission

        def callback(permissions, results):
            if all([res for res in results]):
                print("callback. All permissions granted.")
            else:
                print("callback. Some permissions refused.")

        request_permissions([Permission.ACCESS_COARSE_LOCATION,
                             Permission.ACCESS_FINE_LOCATION, Permission.CALL_PHONE], callback)

    def build(self):
        # Create the screen manager
        pass


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
    latitude = StringProperty("37.7749")
    longitude = StringProperty("122.4194")

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
        self.latitude = str(kwargs['lat'])
        self.longitude = str(kwargs['lon'])
        self.map_view.center_on(self.latitude, self.longitude)


# Run the app
if __name__ == '__main__':
    MainApp().run()
