from laserDetection import detect_laser
from linkDetection import detect_link
import base64
import cv2
import math
import numpy as np
import os
import threading
import time
import zmq



# ------------------------------------------------------------------------
# Server Backend


context = zmq.Context()

footage_socket = context.socket(zmq.SUB)
footage_socket.bind('tcp://*:5555')
footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

targeting_socket = context.socket(zmq.PUB)
targeting_socket.connect('tcp://192.168.0.125:6666')

img = cv2.imread("templates/start.jpg")
laser_coords =  (-1, -1)
link_coords = (-1, -1)
link_pos = (-1, -1)



def laser_processing():
    global laser_coords

    laser_coords = detect_laser(img)



def link_processing():
    global link_coords, link_pos

    link_data = detect_link(img)
    link_coords = link_data[0:2]
    link_pos = link_data[2:]



def process_data():

    while(1):
        laser_processing()
        link_processing()

        coords = ",".join(str(x) for x in laser_coords) + "," + ",".join(str(x) for x in link_coords)
        targeting_socket.send_string(coords)



def receive_images():
    global img

    while(1):
        try:
            frame = footage_socket.recv_string()
            img64 = base64.b64decode(frame)
            npimg = np.fromstring(img64, dtype=np.uint8)
            img = cv2.imdecode(npimg, 1)

        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            return



def main():

    x1 = threading.Thread(target = receive_images, daemon = True)
    x2 = threading.Thread(target = process_data, daemon = True)

    x1.start()
    x2.start()



if __name__ == "__main__":
    main()



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
    retval, buffer = cv2.imencode('.jpg', img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpg'
    return response

@app.errorhandler(404)
def page_not_found(error):
    return "page not found", 404

app.run(debug=True, host='0.0.0.0', use_reloader=False)
