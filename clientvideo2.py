import cv2
import requests as req
import numpy as np
from io import BytesIO
import threading
import time

server_url="http://192.168.1.116:5050/video"
signal_url="http://192.168.1.116:5050/signal"

def key_listener():
    while True:
        user_input=input("Press 's' to send signal, 'q' to quit")
        if user_input == 's':
            try:
                response=req.post(signal_url,data=b'servo')
                print("Signal sent")
            except req.exception.RequestException as e:
                print(f"Error sending signal: {e}")
        elif user_input =='q':
            print("Exiting key listener...")
            break


signal_thread=threading.Thread(target=key_listener)

signal_thread.start()


while True:
    try:
        response = req.get(server_url)
        if response.status_code == 200:
            img_data = BytesIO(response.content)
            img_array = np.frombuffer(img_data.getvalue(), np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  

            if frame is not None:
                
                cv2.imshow('Client2 - Receiving Video', frame)
            else:
                print("Failed to decode the image.")
        else:
            print(f"Failed to get video feed, status code: {response.status_code}")
        
    except Exception as e:
        print(f"Error occurred: {e}")

    if cv2.waitKey(1)==27:
        break
        
cv2.destroyAllWindows()

signal_thread.join()