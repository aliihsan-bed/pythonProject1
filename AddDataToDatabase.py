import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,
{
    'databeseURL' : "https://faceattendacerealtime-43c65-default-rtdb.firebaseio.com/"
})
