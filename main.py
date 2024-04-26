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
from kivy.clock import Clock, mainthread
from plyer import gps
from plyer.utils import platform

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

    gps_location = StringProperty("")
    gps_status = StringProperty("")

    def on_start(self):
        if utils.platform == 'android':
            self.gps_init()

    def locate_current_location(self):
        gps.configure(on_location=self.on_location)
        gps.start(minTime=1000, minDistance=0)

    def on_location(self, **kwargs):
        self.latitude = str(kwargs['lat'])
        self.longitude = str(kwargs['lon'])
        print(self.longitude, self.latitude)

    @mainthread
    def gps_init(self):
        try:
            gps.configure(on_location=self.on_location,
                          on_status=self.on_status)

        except NotImplementedError:
            import traceback
            traceback.print_exc()
            gps_status = 'GPS is not implemented for your platform'

            return gps_status

        if platform == "android":
            print("gps.py: Android detected. Requesting permissions")
            self.request_android_permissions()

    @mainthread
    def start(self, minTime=1000, minDistance=10):
        gps.start(minTime, minDistance)

    @mainthread
    def stop(self):
        gps.stop()

    @mainthread
    def on_location(self, **kwargs):
        map = self.root.ids.mapp
        self.gps_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])

        map.center_on(float(kwargs["lat"]), float(kwargs["lon"]))
        self.latitude = str(float(kwargs["lat"]))
        self.longitude = str(float(kwargs["lon"]))

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

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
    pass



class HomeScreen(MDScreen):
    pass


class MDScreenManager(ScreenManager):
    pass


# Run the app
if __name__ == '__main__':
    MainApp().run()
