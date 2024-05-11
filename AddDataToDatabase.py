import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,
        {
                    'databaseURL':"https://faceattendacerealtime-43c65-default-rtdb.firebaseio.com/"
                })
ref = db.reference('Students')
data = {
    "321654":
        {
            "name":"ali",
            "major" : "yazilim",
            "starting" : 2020,
            "total" : 4,
            "standing":"G",
            "year": "4",
            "last_attendance_time" : "2022-12-12 00:54:34"
        },
    "852741":
        {
            "name":"munzir",
            "major" : "yazilim",
            "starting" : 2021,
            "total" : 5,
            "standing":"G",
            "year": "5",
            "last_attendance_time" : "2022-12-13 00:54:34"
        },
    "963852":
        {
            "name":"elon",
            "major" : "araba",
            "starting" : 2022,
            "total" : 6,
            "standing":"G",
            "year": "6",
            "last_attendance_time" : "2022-12-14 00:54:34"
        }
}

for key,value in data.items():
    ref.child(key).set(value)
