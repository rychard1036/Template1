# firebase_handle.py
import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK
def initialize_firebase():
    cred = credentials.Certificate(r"C:\Users\raymo\Downloads\smartdb-8e02f-firebase-adminsdk-97v2u-9b8af0e661.json")
    firebase_admin.initialize_app(cred)

# Create a new user
def create_user(email, password):
    user = auth.create_user(
        email=email,
        email_verified=False,
        password=password,
        disabled=False)
    print('Successfully created new user:', user.uid)
    return user.uid
