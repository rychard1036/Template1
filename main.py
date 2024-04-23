# Import necessary modules
from kivy import utils
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy_garden.mapview import MapMarkerPopup, MapView, MapSource
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFillRoundFlatIconButton
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from plyer import gps

from markers import markers

if utils.platform != 'android':
    Window.size = (412, 732)


class RowCard(MDCard):
    icon = StringProperty("")
    name = StringProperty("")


# Define the main app class
class MainApp(MDApp):
    size_x, size_y = Window.size
    latitude = StringProperty("-5.767057")
    longitude = StringProperty("34.723747")

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
        self.theme_cls.material_style = "M3"
        return MDScreenManager()


class MapScreen(MDScreen):
    def on_enter(self, *args):
        map_source = MapSource(url="https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        self.ids.mapp.map_source = map_source

        for location_data in markers:
            lat = location_data["lat"]
            lon = location_data["lon"]
            text = location_data["text"]

            popup = MapMarkerPopup(lat=lat, lon=lon, size_hint=(None, None), size=(30, 30))
            popup.add_widget(MDLabel(text=text))
            self.ids.mapp.add_marker(popup)


class HomeScreen(MDScreen):
    pass


class MDScreenManager(ScreenManager):
    pass


# Run the app
if __name__ == '__main__':
    MainApp().run()
