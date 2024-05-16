# Import necessary modules
import firebase_admin
from firebase_admin.auth import create_user
from firebase_handle import create_user, initialize_firebase, auth
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
from kivymd.uix.textfield import MDTextField
from plyer import gps
from plyer.utils import platform

from markers import markers

# Initialize Firebase Admin SDK
initialize_firebase()

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
        for location_data in markers:  # Iterate through the markers imported from markers.py
            latitude = location_data["lat"]
            longitude = location_data["lon"]
            text = location_data["text"]
            self.root.ids.mapp.add_widget(MapMarkerPopup(lon=longitude, lat=latitude))

    def locate_current_location(self, **kwargs):
        print("Markers Starts")
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
    #creating user
    def create_new_user(self, email, password, display_name):
        create_user(email, password, display_name)

    def create_user(self, **kwargs):
        email = self.root.ids.email_field.text
        password = self.root.ids.password_field.text


        if email and password:
            uid = create_user(email, password)
            print("User created with UID:", uid)

    #Authenticate user
    def authenticate_user(self):
        email = self.root.ids.email_field.text
        password = self.root.ids.password_field.text

        try:
            user_name = auth.get_user_by_email(email)
            print('Successfully signed in:', user_name)
            self.root.current = "map"
        except Exception as e:
            print('Failed to sign in:', e)

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
