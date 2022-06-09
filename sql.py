import cv2 #thu vien cv2
import numpy as np
import sqlite3 #thu vien csdl
import os #truy cap he thong

#ham truy cap databas e
def insertOrupdate(id, name):
    #connect voi database
    conn = sqlite3.connect("D:/nhandienguongmat/data.db")

    #lay du lieu
    query = "SELECT * FROM people WHERE ID=" + str(id)
    cusror = conn.execute(query)

    isRecorExist = 0

    for row in cusror:
        isRecorExist = 1

    if(isRecorExist == 0):
        query = "INSERT INTO people (ID, Name) VALUES("+str(id)+",'" +str(name)+"')"
    else:
        query = "UPDATE people SET Name ='"+str(name)+"' WHERE ID ="+ str(id)

    conn.execute(query)
    conn.commit()
    conn.close()
#load thu vien
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
eye_cascade_left = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_lefteye_2splits.xml')
eye_cascade_right = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_righteye_2splits.xml')
videocap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#insert database
id = input("Enter your ID: ")
name = input("Enter your name: ")
insertOrupdate(id, name)

number = 0

while(True):
    ret, frame = videocap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for(x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),1)

        if not os.path.exists('dataSet'):
            os.makedirs('dataSet')

        number += 1

        cv2.imwrite('dataSet/User.'+str(id)+'.'+str(number)+'.jpg', gray[y: y+h, x: x+w])


    #nhan dien mat eyes
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(frame, (ex,ey), (ex+ew, ey+eh), (255,255,255),1)

        if not os.path.exists('dataSet'):
            os.makedirs('dataSet')

        number += 1

        cv2.imwrite('dataSet/User.'+str(id)+'.'+str(number)+'.jpg', gray[ey: ey+eh, ex: ex+ew])

    cv2.imshow('Get Face',frame)
    cv2.waitKey(1)

    if number > 400:
        break

videocap.release()
cv2.destroyAllWindows()