import cv2
import numpy as np
import face_recognition
import os
import urllib.request
import time
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import datetime
import os


def find_encodings(images):

    encodelist = []

    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)

    return encodelist


def FacialRecognition():

    sheet = pd.read_csv('Sheet.csv')
    date = datetime.date.today()
    
    sheet[str(date)] = ['A' for x in range(45)]
    
    sheet.set_index("Reg No")

    URL = "http://10.1.142.112:8080/shot.jpg"
    path = 'AttendanceImages'

    images = []
    ClassNames = []

    mylist = os.listdir(path)

    for file in mylist:

        curImg = cv2.imread(f"{path}\{file}")
        images.append(curImg)
        ClassNames.append(os.path.splitext(file)[0])

    EncodeListKnown = find_encodings(images)

    while True:

        img_arr = np.array(
            bytearray(urllib.request.urlopen(URL).read()), dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)
        imgS = cv2.resize(img, (0, 0), None, 1, 1)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodedCurFram = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceloc in zip(encodedCurFram, facesCurFrame):

            matches = face_recognition.compare_faces(
                EncodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(
                EncodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex] and faceDis[matchIndex]<0.5:
                name = ClassNames[matchIndex].upper()

                for i in range(45):
                    if str(sheet.iloc[i, 0]) == name:
                        sheet.at[i, str(date)] = 'P'
                        break

                y1, x2, y2, x1 = faceloc
                y1, x2, y2, x1 = int(
                    y1*1), int(x2*1), int(y2*1), int(x1*1)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y1-35), (x2, y2), (0, 255, 0), 7)
                cv2.putText(img, name, (x1+6, y1-6),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

        cv2.imshow("Attendance System", img)
        key = cv2.waitKey(1)
        if(key == 27):
            os.remove("Sheet.csv")
            sheet.to_csv("Sheet.csv",index=False)

            break
