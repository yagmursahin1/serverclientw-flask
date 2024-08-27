import cv2
import requests as req
from io import BytesIO
import time
import threading

server_url="http://192.168.1.116:5050/video_feed" 
signal_url="http://192.168.1.116:5050/signal" 

global frame_to_send
frame_to_send=None


def send_video():
    global frame_to_send
    fps_send=5
    interval_send=1.0/fps_send

    while True:
        if frame_to_send is not None:
            try:
                response = req.post(server_url, data=frame_to_send)
                print(f"Server yanıt kodu: {response.status_code}")
            except req.exceptions.RequestException as e:
                print(f"POST isteği sırasında hata: {e}")
        time.sleep(interval_send)


def handle_signals():
    while True:
        try:
            signal_response=req.get(signal_url)
            if signal_response.status_code==200:
                signal=signal_response.text
                if signal =='servo':
                    print("servo açıldı")
                    req.post(signal_url,data=b'')
        except req.exceptions.RequestException as e:
            print(f"GET isteği sırasında hata: {e}")
        time.sleep(1)

cap=cv2.VideoCapture(0)
if not cap.isOpened():
    print("Kamera açılamadı.")
    exit()


video_thread=threading.Thread(target=send_video)
signal_thread=threading.Thread(target=handle_signals)

video_thread.start()
signal_thread.start()

while True:
    ret,frame=cap.read()
    if not ret:
        break

    _, buffer=cv2.imencode('.jpg',frame)
    frame_to_send= BytesIO(buffer).getvalue()

    cv2.imshow('Client1-Sending Video',frame)

    if cv2.waitKey(1)==27:
        break
    

cap.release()
cv2.destroyAllWindows()


video_thread.join()
signal_thread.join()
