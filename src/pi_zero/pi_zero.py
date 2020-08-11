from picamera.array import PiRGBArray
from picamera import PiCamera
import base64
import cv2
import io
import os
import numpy as np
import threading
import time
import zmq



context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://192.168.0.100:5555')

targeting_socket = context.socket(zmq.SUB)
targeting_socket.bind('tcp://*:6666')
targeting_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

camera = PiCamera()
camera.resolution = (960, 720)
camera.framerate = 60
camera.vflip = True
camera.hflip = True

rawCapture = PiRGBArray(camera, size = (960, 720))

laser_coords = (-1, -1)
link_coords = (-1, -1)



def send_frames():

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        try:
            image = frame.array
            encoded, buffer = cv2.imencode('.jpg', image)
            jpg_as_text = base64.b64encode(buffer)
            footage_socket.send(jpg_as_text)
            rawCapture.truncate(0)

        except KeyboardInterrupt:
            break



def receive_data():
    global laser_coords, link_coords

    while(1):
        try:
            coords = targeting_socket.recv_string()
            coords = coords.split(",")
            laser_coords = (int(coords[0]), int(coords[1]))
            link_coords = (int(coords[2]), int(coords[3]))
            print("Laser Coords: " + str(laser_coords))
            print("Link Coords: " + str(link_coords))
            print("-----")

        except KeyboardInterrupt:
            break



def main():

    x1 = threading.Thread(target = send_frames, daemon = False)
    x2 = threading.Thread(target = receive_data, daemon = True)

    x1.start()
    x2.start()



if __name__ == "__main__":
    main()
