#************************ MODULES, METHODS **************************************************
from cv2 import (VideoCapture, CascadeClassifier, cvtColor, VideoWriter,
                  VideoWriter_fourcc, COLOR_BGR2GRAY,imshow,
                 waitKey, destroyAllWindows)

from datetime import datetime
from time import time

from cv2.data import haarcascades
from os import mkdir
from os.path import exists

#******************************** MAIN ********************************************************
if __name__ == '__main__':
    cap = VideoCapture(0)
    # Default face and body cascade detections
    face_cascade = CascadeClassifier(haarcascades + 'haarcascade_frontalface_default.xml')
    body_cascade = CascadeClassifier(haarcascades + "haarcascade_fullbody.xml")

    detection = False
    detection_stopped_time = None
    timer_started = False

    frame_size = (int(cap.get(3)), int(cap.get(4)))
    # We want to write a file .mp4 type
    fourcc = VideoWriter_fourcc(*"mp4v")

    while True:
        ret, frame = cap.read()
        gray = cvtColor(frame, COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        bodies = body_cascade.detectMultiScale(gray, 1.3, 5)

        SECONDS_TO_RECORD_AFTER_DETECTION = 3

        """
            if your camera checks your face or your body,
            started recording and create a new file with
            the current time and extension .mp4
        """
        if len(faces) + len(bodies) > 0:
            if detection:
                timer_started = False
            else:
                detection = True
                if not exists('assets'):
                    print('\nassets not exists. Creating assets...\n')
                    mkdir('assets')
                current_time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                out = VideoWriter(f'assets/{current_time}.mp4', fourcc, 20, frame_size)
                print('Started Recording!')
        elif detection:
            if timer_started:
                """ 
                        if your camera doesn't detect your face for three seconds, 
                        stop recording and write the file
                """
                if time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                    detection = False
                    timer_started = False
                    out.release()
                    print('Stop Recording!')
            else:
                timer_started = True
                detection_stopped_time = time()

        if detection:
            out.write(frame)

        #display the frame of your camera
        imshow("Camera", frame)

        key = waitKey(1)
        if key == 27:
            break

    """
        release resources when you close the
        video stream and destroy the opencv
    """
    out.release()
    cap.release()
    destroyAllWindows()
