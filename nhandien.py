import cv2
import sqlite3


#thu vien nhan dien khuon mat va thu vien thu vien training nhan dien
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()

#thu vien nhan dien mắt
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
eye_cascade_left = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_lefteye_2splits.xml')
eye_cascade_right = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_righteye_2splits.xml')

recognizer.read('D:/nhandienguongmat/recognizer/trainningData.yml')

#lay thong tin khuon mat trong db
def getProfile(id):

    #connect database
    conn = sqlite3.connect("D:/nhandienguongmat/data.db")
    query = "SELECT * FROM people WHERE ID ="+str(id)
    cursor = conn.execute(query)

    #tao bien luu gia tri lay tu db
    profile = None
    for row in cursor:
        profile = row

    #unconnect
    conn.close()
    return profile

cap = cv2.VideoCapture(0)
#dat font chu
font = cv2.FONT_HERSHEY_COMPLEX

while(True):

    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame,(x, y), (x + w, y + h), (0, 255, 0), 1)

        roi_gray = gray[y: y+h, x: x+w]
        #nhan dien
        id, exactly = recognizer.predict(roi_gray)
        #kiem tra do chinh xac
        if exactly < 400:
            profile = getProfile(id)

            if(profile != None):
                cv2.putText(frame, ""+str(profile[1]),(x + 10 , y + h + 30), font, 1, (150, 250 ,150),1)
        else:
            cv2.putText(frame, "Unknow", (x + 10, y + h + 30), font, 1, (0, 255, 0), 1)

    #nhan dien mat eyes
    eyes = eye_cascade.detectMultiScale(gray)
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(frame, (ex,ey), (ex+ew, ey+eh), (255,255,255),1)

    cv2.imshow('Recognizer', frame)
    if(cv2.waitKey(1) == ord('q')):
        break

cap.release()
cv2.destroyAllWindows