from dbConnection import create_db, insert_data
from laserDetection import detect_laser
from linkDetection import detect_link
import base64
import cv2
import numpy as np
import threading
import zmq



# ------------------------------------------------------------------------
# Server Backend


context = zmq.Context()

footage_socket = context.socket(zmq.SUB)
footage_socket.bind('tcp://*:5555')
footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

targeting_socket = context.socket(zmq.PUB)
targeting_socket.connect('tcp://192.168.0.125:6666')

img = cv2.imread('./data/intro.jpg')
isIntroImg = True

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
        if isIntroImg:
            continue

        laser_processing()
        link_processing()

        coords = ",".join(str(x) for x in laser_coords) + "," + ",".join(str(x) for x in link_coords)
        targeting_socket.send_string(coords)
        insert_data(laser_coords, link_coords, link_pos)



def receive_images():
    global img, isIntroImg

    while(1):
        try:
            frame = footage_socket.recv_string()
            img64 = base64.b64decode(frame)
            npimg = np.fromstring(img64, dtype=np.uint8)
            img = cv2.imdecode(npimg, 1)
            isIntroImg = False

        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            return



def main():

    create_db()

    x1 = threading.Thread(target = receive_images, daemon = True)
    x2 = threading.Thread(target = process_data, daemon = True)

    x1.start()
    x2.start()



if __name__ == "__main__":
    main()



# ------------------------------------------------------------------------
# Flask Webserver


from flask import Flask, request, make_response, render_template, send_file
from flask_cors import CORS, cross_origin
import logging

app = Flask(__name__)
CORS(app)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/image')
def image():
    retval, buffer = cv2.imencode('.jpg', img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpg'
    return response

app.run(debug=True, host='0.0.0.0', use_reloader=False)
