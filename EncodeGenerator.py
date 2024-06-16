import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendacerealtime-43c65-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendacerealtime-43c65.appspot.com"
})

# Öğrenci resimlerini yükleme
folderPath = 'Images'
pathList = os.listdir(folderPath)

imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print(studentIds)

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        if len(encodings) > 0:
            encode = encodings[0]
            encodeList.append(encode)
        else:
            print(f"Yüz algılanamadı, görüntü atlandı: {img}")
    return encodeList

print("Kodlama başlatılıyor...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Kodlama tamamlandı")

with open("EncodeFile.p", 'wb') as file:
    pickle.dump(encodeListKnownWithIds, file)
print("Dosya kaydedildi")
