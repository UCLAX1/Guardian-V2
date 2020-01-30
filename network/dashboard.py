import cv2
import threading
import zmq
import base64
import numpy as np
import os

# global variable
Image = cv2.imread("templates/start.jpg")

context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
footage_socket.bind('tcp://*:5555')
footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))


def downloading_images():
    global Image
    i = 0
    print("thread started")
    while(1):
        try:
            frame = footage_socket.recv_string()
            img64 = base64.b64decode(frame)
            npimg = np.fromstring(img64, dtype=np.uint8)
            Image = cv2.imdecode(npimg, 1)
            i += 1
            print("frame ",i)

            # cv2.imwrite('t/i'+str(i)+'.jpg', Image)
            # cv2.imwrite('t/temp/image.jpg', Image)
            # os.rename("t/temp/image.jpg", "t/image.jpg")
            #cv2.imshow("Stream", Image)

        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            return

x = threading.Thread(target=downloading_images, daemon=True)
x.start()




# ------------------------------------------------------------------------
# Webserver using flask
from flask import Flask, request, make_response, render_template, send_file


app = Flask(__name__)
img = cv2.imread("templates/image.jpg")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start.jpg')
def start():
    return send_file('templates/start.jpg')

@app.route('/image.jpg')
def image():
    retval, buffer = cv2.imencode('.jpg', Image)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpg'
    return response

@app.errorhandler(404)
def page_not_found(error):
    return "okay boomer", 404


app.run(debug=True, host='0.0.0.0',use_reloader=False)
