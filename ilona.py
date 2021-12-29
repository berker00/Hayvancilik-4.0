import cv2
import numpy as np
import dlib
import pymongo
import datetime

#tarih
dir(datetime.datetime)
an = datetime.datetime.now()
tarih = datetime.datetime.ctime(an)

#server
myclient = pymongo.MongoClient("mongodb+srv://beko:beko1@snr.wfbea.mongodb.net/myFirstDatabase?retryWrites=true&w=majority") 
mydb = myclient["ex1"]
mycol = mydb["ex"]


#video
cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    i = 0

    for face in faces:
        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()
        cv2.rectangle(frame, (x,y), (x1, y1), (0, 255), 2)
        i = i+1
        cv2.putText(frame,'koyun ID'+str(i), (x-10, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        print(face, i)
    cv2.imshow('Bekocam', frame)
    if i == 10:
        mydict = {
            "Koyun_id" : i,
            "Tarih" : tarih,
        }
        x = mycol.insert_one(mydict)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()