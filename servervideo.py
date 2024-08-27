from flask import Flask, Response, request

app=Flask(__name__)
frame=None
signal_to_client1=None


@app.route('/video_feed',methods=['POST'])
def upload_video():
    global frame
    frame=request.data
    print(f"Received {len(frame)} bytes of data")
    return  f"Received {len(frame)} bytes of data"


@app.route('/video',methods=['GET'])
def video_feed():
    if frame is None:
        return "No video feed available"
    return Response(frame,mimetype='image/jpeg')
    
@app.route('/signal',methods=['POST'])
def receive_signal():
    global signal_to_client1
    signal_to_client1=request.data.decode()
    return ''

@app.route('/signal',methods=['GET'])
def send_signal():
    if signal_to_client1 is None:
        return Response(status=204)
    return Response(signal_to_client1,mimetype='text/plain')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5050,debug=True)
