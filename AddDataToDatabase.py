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
            "starting_year" : 2020,
            "total_attendance" : 4,
            "standing":"G",
            "year": "4",
            "last_attendance_time" : "2022-12-12 00:54:34"
        },
    "852741":
        {
            "name":"munzir",
            "major" : "yazilim",
            "starting_year" : 2021,
            "total_attendance" : 5,
            "standing":"G",
            "year": "5",
            "last_attendance_time" : "2022-12-13 00:54:34"
        },
    "963852":
        {
            "name":"elon",
            "major" : "araba",
            "starting_year" : 2022,
            "total_attendance" : 6,
            "standing":"G",
            "year": "6",
            "last_attendance_time" : "2022-12-14 00:54:34"
        },
    "111111":
        {
            "name": "ronaldo",
            "major": "futbol",
            "starting_year": 2023,
            "total_attendance": 6,
            "standing": "G",
            "year": "6",
            "last_attendance_time": "2022-12-15 00:54:34"
        }

}

for key,value in data.items():
    ref.child(key).set(value)

