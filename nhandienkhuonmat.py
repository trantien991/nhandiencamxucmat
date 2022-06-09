import cv2 


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
eye_cascade_left = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_lefteye_2splits.xml')
eye_cascade_right = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_righteye_2splits.xml')


videocap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while(True):

    
    ret, frame = videocap.read()

    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

   
    faces = face_cascade.detectMultiScale(gray)
    
    for(x,y,w,h) in faces:

        
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),1)

        
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        

    
    cv2.imshow('EYE',frame)

    eyes = eye_cascade.detectMultiScale(gray)
    
    for(x,y,w,h) in eyes:

        
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,255,255),1)

        
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        


    
    cv2.imshow('EYE',frame)



    
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

videocap.release()

cv2.destroyAllWindows()

