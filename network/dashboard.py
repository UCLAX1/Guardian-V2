import cv2
import threading
import zmq
import base64
import numpy as np
import os
import time
import math

Image = cv2.imread("templates/start.jpg") # image cv2
Lazer = [1.0,2.0,3.0] # lazer x,y,r
Link =  [1.0,2.0,3.0] # not used yet - link position

# ------------------------------------------------------------------------
# lazer detection functions [received from audi]

def detect_lazer(frame): #input an image, returns and prints the detected coordinate. Returns empty list if none found.
      
  ratio = 13 #3
  kernel_size = 3 #
  low_threshold = 30 #30
  img_blur = cv2.blur(frame, (3,3)) #3,3
  detected_edges = cv2.Canny(img_blur, low_threshold, low_threshold*ratio, kernel_size)
  mask = detected_edges != 0
  edges = frame * (mask[:,:,None].astype(frame.dtype)) #numpy array
  
  gray = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)

  circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 50, param1=1, param2=13, minRadius=0, maxRadius=30) #max 60 pixel circle #50 , param2 small = more false circles
  
  if circles.ndim == 1:#one circle
      #print(circles)
      return circles

  
  elif circles.ndim == 3:
      #red_circles = []
      result = np.asarray([])
      min_dist = float("inf")
      
      for circle in circles[0, :]: #cirlce = (x, y ,radius)
          x = int(circle[0])
          y = int(circle[1])
          r,g,b = frame[y,x]
          
  
      
          rgb = frame[y,x]
          rgb_pixel = rgb.reshape((1,1,3))
          hsv = cv2.cvtColor(rgb_pixel, cv2.COLOR_BGR2HSV)
          h = hsv[0,0,0]
          s = hsv[0,0,1]
          v = hsv[0,0,2]
          
          red = (h < 200) and (s < 110) and (v>100)
          if red:
              squares = (h-81)**2 + (s-30)**2 + (v-250)**2
              dist = math.sqrt( squares )
              if dist < min_dist:
                  result = circle
                  min_dist = dist
     
      if result.shape != (3,) :
          #print("failed to find white or red center")
          pass
      
      #print(coord)
      #print(result)
      return result
                  
      #n = len(red_circles)
      #red_circles = np.array(red_circles).reshape(1,n,3)
      #return red_circles
        
          #hsv range:  vide 1 first 84 frames result
          #h: 0-200 (0-170) mean: 81, median 90
          #s: 0-110 (0-85) mean: 10 median: 5. 36?
          #v: 120-255 (129-255) mean: 250, median 255
  else:
      #print("Skipping filtering because function detect_cirlces detected no circles")
      result = np.asarray([])
      #print(result)
      return result


# lazer thread
def image_processing():
    global Lazer

    print("thread2 started")
    # process Lazer
    while(1):
        try:
            result = detect_lazer(Image)
            if result.size != 0: Lazer = result
            else: Lazer = [0,0,0]
            
            print("lazer",Lazer)
            time.sleep(0.05)
        except KeyboardInterrupt:
            return


# ------------------------------------------------------------------------
# Image receiving network

context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
footage_socket.bind('tcp://*:5555')
footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

# network thread
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


# ------------------------------------------------------------------------
# Starting Threads

x = threading.Thread(target=downloading_images, daemon=True)
x.start()

x2 = threading.Thread(target=image_processing, daemon=True)
x2.start()


# ------------------------------------------------------------------------
# Webserver using flask
from flask import Flask, request, make_response, render_template, send_file


app = Flask(__name__)

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

@app.route('/data.txt')
def data():
    return str(Lazer)[1:-1]

@app.errorhandler(404)
def page_not_found(error):
    return "okay boomer", 404


app.run(debug=True, host='0.0.0.0',use_reloader=False)
