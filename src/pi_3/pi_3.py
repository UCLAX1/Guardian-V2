import io
import numpy as np
import os
import threading
import zmq



context = zmq.Context()
controls_socket = context.socket(zmq.SUB)
controls_socket.bind('tcp://*:7777')
controls_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

# Format: (distance, angle)
input_data = (-1, -1)
detected_data = (-1, -1)



def receive_data():
    global input_data, detected_data

    while(1):
        try:
            data = controls_socket.recv_string()

            if "UserInput - " in data:
                input_distance = int(data.split("Distance: ")[1].split(", Angle: ")[0])
                input_angle = int(data.split("Angle: ")[1])
                input_data = (input_distance, input_angle)
                print("User Input Data: " + str(input_data))
            elif "Detected - " in data:
                detected_distance = float(data.split("Distance: ")[1].split(", Angle: ")[0])
                detected_angle = float(data.split("Angle: ")[1])
                detected_data = (detected_distance, detected_angle)
                print("Detected Data: " + str(detected_data))

        except KeyboardInterrupt:
            break



def main():

    x1 = threading.Thread(target = receive_data, daemon = False)

    x1.start()



if __name__ == "__main__":
    main()
