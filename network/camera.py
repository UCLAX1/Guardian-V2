
import base64
import cv2
import zmq
import time

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://localhost:5555')
#footage_socket.connect('tcp://192.168.0.100:5555')

camera = cv2.VideoCapture("myVideo.mp4")  # init the camera

i = 0
while True:
    try:
        grabbed, frame = camera.read()  # grab the current frame
        if frame is None:
            break;
        i+=1
        print(str(i)+" "+str(frame.shape))
        encoded, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)
        footage_socket.send(jpg_as_text)

    except KeyboardInterrupt:
        camera.release()
        cv2.destroyAllWindows()
        break
