import cv2 #type: ignore
import numpy as np #type: ignore
from simple_facerec import SimpleFacerec
from datetime import datetime
import os

# Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open( 'Attendance'+current_date+'.csv','w+',newline = '' )
f.write('Name,Time')
f.close()

# add this function... call it in 'Detect Faces'
def markAttendance(name):
    with open('Attendance'+current_date+'.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList and name != 'Unknown':
            now = datetime.now()
            dtString = now.strftime("%H:%M:%S")
            f.writelines(f'\n{name},{dtString}')

# Load Camera

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Detect faces
    face_locations, face_names = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,200), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,0,200), 4)

        markAttendance(name)

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()