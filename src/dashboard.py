import cv2
import threading
import zmq
import base64
import numpy as np
import os
import time
import math

from laserDetection import detect_laser
from linkDetection import detect_link

Image = cv2.imread("templates/start.jpg")
Link =  (-1, -1)
Laser = (-1, -1, -1, -1)


def laser_processing():
    global Laser
    Laser = detect_laser(Image)


def link_processing():
    global Link
    Link = detect_link(Image)


def combo_processing():
    global Laser, Link

    while(1):
        laser_processing()
        link_processing()
        print("Laser: " + str(Laser))
        print("Link: " + str(Link))
        print("---")
        time.sleep(0.05)




# ------------------------------------------------------------------------
# Receiving Images

context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
footage_socket.bind('tcp://*:5555')
footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))


def downloading_images():
    global Image
    i = 0
    while(1):
        try:
            frame = footage_socket.recv_string()
            img64 = base64.b64decode(frame)
            npimg = np.fromstring(img64, dtype=np.uint8)
            Image = cv2.imdecode(npimg, 1)
            i += 1

        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            return


# ------------------------------------------------------------------------
# Starting Threads

x1 = threading.Thread(target=downloading_images, daemon=True)
x2 = threading.Thread(target=combo_processing, daemon=True)

x1.start()
x2.start()


# ------------------------------------------------------------------------
# Flask Webserver

from flask import Flask, request, make_response, render_template, send_file
import logging

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

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
