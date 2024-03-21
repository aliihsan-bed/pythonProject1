import cv2
import face_recognition
import pickle
import os


# importing student images
folderPath = 'Images'
PathList = os.listdir(folderPath)

imgList = []
stundetIds = []
for path in PathList:
    imgList.append(cv2.imread((os.path.join(folderPath, path))))

    stundetIds.append(os.path.splitext(path)[0])

print(stundetIds)

def findEncoding(imagesList):
    encodeList=[]
    for img in imagesList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

print("encoding started...")
encodeListKnown = findEncoding((imgList))
encodeListKnownWithIds = [encodeListKnown, stundetIds]
print("encoding Complete")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")