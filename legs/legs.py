import numpy as np
import time
import path

SIMULATION = True
SERVOS_CONNECTED = True
kit1, kit2 = None, None
try:
    from adafruit_servokit import ServoKit
except:
    print("Servo Library Failed to load")
try:
    kit1 = ServoKit(channels=16,address=0x40)
    kit2 = ServoKit(channels=16,address=0x41)
    #hat_map = [1,1,1,2,2,2]
    #pin_map =[[0,1,2],[3,4,5],[6,7,8],[7,8,9],[10,11,12],[13,14,15]]
except:
    print("Servos Disabled")
    SERVOS_CONNECTED = False
    

class guardian:
    def __init__ (self, zeta = [0,0,0], DH = np.array([]), pathOffsets = [0.08,-0.02], ts=0.01):
        self.legs = []
        self.zeta = zeta    
        self.DH = DH if np.shape(DH)[0] != 0 else np.array([[0.1009,0,0],
				                                            [0.03963,-np.pi/2, 0],
				                                            [0.07755,0,0],
				                                            [0.14006,0,0]])
        self.pathOffsets = pathOffsets
        self.moveSteps = [0,0,0,0]
        self.cur_pos = 0
        self.ts = ts
        self.setTurretThrottle(0)
        for i in range(6):
            self.legs.append(leg(i+1,self.DH))
            #self.legs.append(leg(i+1,self.DH))
        self.dx = path.path_F[0,0] - path.path_F[1,0]
        #print(self.dx)
        self.dphi = -(np.arctan2(path.path_CCW[0,0],path.path_CCW[0,1]+self.DH[0,0]) - np.arctan2(path.path_CCW[1,0],path.path_CCW[1,1]+self.DH[0,0]))
        #print(self.dphi)

    def __call__ (self):
        return self.legs

    def resetLegs (self):
        global kit1, kit2, SERVOS_CONNECTED
        if SERVOS_CONNECTED:
            for i in range(16):
                kit1.servo[i].angle = 90
                kit2.servo[i].angle = 90
            return 1
        return -1

    def setTurretThrottle(self, val):
        if val < -1 or val > 1:
            print("Turret Throttle must be between -1 and 1.")
            return -1
        global kit2, SERVOS_CONNECTED
        if SERVOS_CONNECTED:
            self.turretThrottle = val
            kit2.continuous_servo[9].throttle = val
            return 1
        return -1

    def nextPos (self):
        global kit1, kit2, SERVOS_CONNECTED
        vals = [0,0,0,0,0,0]
        for i in range(3):
            vals[i] = self.legs[i].nextPos()
            vals[i+3] = self.legs[i+3].nextPos()
            if SERVOS_CONNECTED:
                kit1.servo[3*i].angle   = 90 - self.legs[i].theta[self.legs[i].currentPos,0]*180/np.pi
                kit2.servo[3*i].angle   = 90 - self.legs[i+3].theta[self.legs[i+3].currentPos,0]*180/np.pi
                kit1.servo[3*i+1].angle = 90 - self.legs[i].theta[self.legs[i].currentPos,1]*180/np.pi
                kit2.servo[3*i+1].angle = 90 - self.legs[i+3].theta[self.legs[i+3].currentPos,1]*180/np.pi
                kit1.servo[3*i+2].angle = 90 - self.legs[i].theta[self.legs[i].currentPos,2]*180/np.pi
                kit2.servo[3*i+2].angle = 90 - self.legs[i+3].theta[self.legs[i+3].currentPos,2]*180/np.pi
            
        if -1 not in vals:
            if self.legs[0].currentPos > self.moveSteps[0]\
                and self.legs[0].currentPos <= self.moveSteps[0] + self.moveSteps[1]:
                    self.zeta[2] += self.dphi
            elif self.legs[0].currentPos > self.moveSteps[0] + self.moveSteps[1] + self.moveSteps[2]\
                and self.legs[0].currentPos <= self.moveSteps[0] + self.moveSteps[1] + self.moveSteps[2] + self.moveSteps[3]:
                    self.zeta[0] += self.dx*np.cos(self.zeta[2])
                    self.zeta[1] += self.dx*np.sin(self.zeta[2])

    def moveTo (self, x, y, RESET_AFTER = False):
        self.calculateMoveTrajectory(x, y, RESET_AFTER)
        for i in range(self.totalPathLength):
            time.sleep(self.ts)
            self.nextPos()

    def rotate (self, phi, RESET_AFTER = False):
        self.calculateRotateTrajectory(phi, RESET_AFTER)
        for i in range(self.totalPathLength):
            time.sleep(self.ts)
            self.nextPos()

    def calculateRotateTrajectory (self, phi, RESET_AFTER = False):
        if phi == 0: return
        delays = [0,16,32,0,16,32]
        self.moveSteps = [0,0,0,0,0]
        prep_paths1 = {
            0: np.empty((0,3)),
            1: np.empty((0,3)),
            2: np.empty((0,3)),
            3: np.empty((0,3)),
            4: np.empty((0,3)),
            5: np.empty((0,3)),
        }
        rot_paths = {
            0: np.empty((0,3)),
            1: np.empty((0,3)),
            2: np.empty((0,3)),
            3: np.empty((0,3)),
            4: np.empty((0,3)),
            5: np.empty((0,3)),
        }
        #Rotate
        self.dphi = -(np.arctan2(path.path_CCW[0,0],path.path_CCW[0,1]+self.DH[0,0]) - np.arctan2(path.path_CCW[1,0],path.path_CCW[1,1]+self.DH[0,0]))
        N = int(np.ceil(phi/self.dphi))
        if N != 0:
            if N > 0:
                rotation_path = np.copy(path.path_CCW)
            else: 
                rotation_path = np.copy(path.reflect(path.path_CCW,1))
                self.dphi = -self.dphi
                N = -N
            for i in range(6):
                delayed_path = path.delay(rotation_path,delays[i])
                pathLength = np.shape(delayed_path)[0]
                temp_path = np.array([delayed_path[0,0:3]])
                for j in range(N):
                    temp_path = np.append(temp_path, [delayed_path[(j+1)%pathLength,0:3]], 0)
                rot_paths[i] = temp_path
        self.moveSteps[1] = N
        #Prep Legs For Rotation
        if self.moveSteps[1] > 0:
            temp_path = {
                0: path.path_Jump(self.legs[0].path[self.legs[0].currentPos,0:3],rot_paths[0][0,0:3]),
                1: path.path_Jump(self.legs[1].path[self.legs[1].currentPos,0:3],rot_paths[1][0,0:3]),
                2: path.path_Jump(self.legs[2].path[self.legs[2].currentPos,0:3],rot_paths[2][0,0:3]),
                3: path.path_Jump(self.legs[3].path[self.legs[3].currentPos,0:3],rot_paths[3][0,0:3]),
                4: path.path_Jump(self.legs[4].path[self.legs[4].currentPos,0:3],rot_paths[4][0,0:3]),
                5: path.path_Jump(self.legs[5].path[self.legs[5].currentPos,0:3],rot_paths[5][0,0:3])
            }
            self.moveSteps[0] = 1
            N_jump = [np.shape(temp_path[0])[0],
                      np.shape(temp_path[1])[0],
                      np.shape(temp_path[2])[0],
                      np.shape(temp_path[3])[0],
                      np.shape(temp_path[4])[0],
                      np.shape(temp_path[5])[0]]
            for i in range(6):
                prep_paths1[i] = np.append(prep_paths1[i],[self.legs[i].path[self.legs[i].currentPos,0:3]],0)
            for i in range(3):
                prep_paths1[i] = np.append(prep_paths1[i],temp_path[i],0)
                prep_paths1[i+3] = np.append(prep_paths1[i+3],temp_path[i+3],0)
                for j in range(6):
                    if N_jump[i] > N_jump[i+3]:
                        last_pos = prep_paths1[j][np.shape(prep_paths1[j])[0]-1,0:3]
                        if j == i+3:
                            for k in range(N_jump[i] - N_jump[i+3]):
                                prep_paths1[j] = np.append(prep_paths1[j],[last_pos],0)
                        elif j != i:
                            for k in range(N_jump[i]):
                                prep_paths1[j] = np.append(prep_paths1[j],[last_pos],0)
                    else:
                        last_pos = prep_paths1[j][np.shape(prep_paths1[j])[0]-1,0:3]
                        if j == i:
                            for k in range(N_jump[i+3] - N_jump[i]):
                                prep_paths1[j] = np.append(prep_paths1[j],[last_pos],0)
                        elif j != i+3:
                            for k in range(N_jump[i+3]):
                                prep_paths1[j] = np.append(prep_paths1[j],[last_pos],0)
            self.moveSteps[0] += np.sum([np.max([N_jump[0],N_jump[3]]),np.max([N_jump[1],N_jump[4]]),np.max([N_jump[2],N_jump[5]])])
        
        #Reset Legs After
        if RESET_AFTER:
            reset_paths = {
                0: np.empty((0,3)),
                1: np.empty((0,3)),
                2: np.empty((0,3)),
                3: np.empty((0,3)),
                4: np.empty((0,3)),
                5: np.empty((0,3)),
            }   
            temp_path = {
                0: path.path_Jump(rot_paths[0][self.moveSteps[1],0:3],[0.1,0,-0.17]),
                1: path.path_Jump(rot_paths[1][self.moveSteps[1],0:3],[0.1,0,-0.17]),
                2: path.path_Jump(rot_paths[2][self.moveSteps[1],0:3],[0.1,0,-0.17]),
                3: path.path_Jump(rot_paths[3][self.moveSteps[1],0:3],[0.1,0,-0.17]),
                4: path.path_Jump(rot_paths[4][self.moveSteps[1],0:3],[0.1,0,-0.17]),
                5: path.path_Jump(rot_paths[5][self.moveSteps[1],0:3],[0.1,0,-0.17])
            }
            for i in range(6):
                reset_paths[i] = np.append(reset_paths[i],[rot_paths[i][self.moveSteps[1],0:3]],0)

            N_jump = [np.shape(temp_path[0])[0],
                      np.shape(temp_path[1])[0],
                      np.shape(temp_path[2])[0],
                      np.shape(temp_path[3])[0],
                      np.shape(temp_path[4])[0],
                      np.shape(temp_path[5])[0]]
        
            for i in range(3):
                reset_paths[i] = np.append(reset_paths[i],temp_path[i],0)
                reset_paths[i+3] = np.append(reset_paths[i+3],temp_path[i+3],0)
                for j in range(6):
                    if N_jump[i] > N_jump[i+3]:
                        last_pos = reset_paths[j][np.shape(reset_paths[j])[0]-1,0:3]
                        if j == i+3:
                            for k in range(N_jump[i] - N_jump[i+3]):
                                reset_paths[j] = np.append(reset_paths[j],[last_pos],0)
                        elif j != i:
                            for k in range(N_jump[i]):
                                reset_paths[j] = np.append(reset_paths[j],[last_pos],0)
                    else:
                        last_pos = reset_paths[j][np.shape(reset_paths[j])[0]-1,0:3]
                        if j == i:
                            for k in range(N_jump[i+3] - N_jump[i]):
                                reset_paths[j] = np.append(reset_paths[j],[last_pos],0)
                        elif j != i+3:
                            for k in range(N_jump[i+3]):
                                reset_paths[j] = np.append(reset_paths[j],[last_pos],0)
            self.moveSteps[4] = np.sum([np.max([N_jump[0],N_jump[3]]),np.max([N_jump[1],N_jump[4]]),np.max([N_jump[2],N_jump[5]])])
            #Combine All the Paths
            for i in range(6): self.legs[i].changePath(np.append(prep_paths1[i],
                                                        np.append(rot_paths[i], reset_paths[i],0),0))
        else:
            #Combine All the Paths
            for i in range(6): self.legs[i].changePath(np.append(prep_paths1[i], rot_paths[i],0))
        #print(self.moveSteps)
        self.totalPathLength = self.legs[0].pathLength


    def calculateMoveTrajectory (self, x, y, RESET_AFTER = False):
        delays = [0,16,32,0,16,32]
        prep_paths1 = {
            0: np.empty((0,3)),
            1: np.empty((0,3)),
            2: np.empty((0,3)),
            3: np.empty((0,3)),
            4: np.empty((0,3)),
            5: np.empty((0,3)),
        }
        rot_paths = {
            0: np.empty((0,3)),
            1: np.empty((0,3)),
            2: np.empty((0,3)),
            3: np.empty((0,3)),
            4: np.empty((0,3)),
            5: np.empty((0,3)),
        }
        prep_paths2 = {
            0: np.empty((0,3)),
            1: np.empty((0,3)),
            2: np.empty((0,3)),
            3: np.empty((0,3)),
            4: np.empty((0,3)),
            5: np.empty((0,3)),
        }
        lin_paths = {
            0: np.empty((0,3)),
            1: np.empty((0,3)),
            2: np.empty((0,3)),
            3: np.empty((0,3)),
            4: np.empty((0,3)),
            5: np.empty((0,3)),
        }
        #Rotate
        phi =  np.arctan2(y - self.zeta[1],x - self.zeta[0])
        phi = np.unwrap([0,phi - self.zeta[2]])[1]
        self.dphi = -(np.arctan2(path.path_CCW[0,0],path.path_CCW[0,1]+self.DH[0,0]) - np.arctan2(path.path_CCW[1,0],path.path_CCW[1,1]+self.DH[0,0]))
        N = int(np.ceil(phi/self.dphi))
        if N != 0:
            if N > 0:
                rotation_path = np.copy(path.path_CCW)
            else: 
                rotation_path = np.copy(path.reflect(path.path_CCW,1))
                self.dphi = -self.dphi
                N = -N
            for i in range(6):
                delayed_path = path.delay(rotation_path,delays[i])
                pathLength = np.shape(delayed_path)[0]
                temp_path = np.array([delayed_path[0,0:3]])
                for j in range(N):
                    temp_path = np.append(temp_path, [delayed_path[(j+1)%pathLength,0:3]], 0)
                rot_paths[i] = temp_path
        self.moveSteps[1] = N
        #Prep Legs For Rotation
        if self.moveSteps[1] > 0:
            temp_path = {
                0: path.path_Jump(self.legs[0].path[self.legs[0].currentPos,0:3],rot_paths[0][0,0:3]),
                1: path.path_Jump(self.legs[1].path[self.legs[1].currentPos,0:3],rot_paths[1][0,0:3]),
                2: path.path_Jump(self.legs[2].path[self.legs[2].currentPos,0:3],rot_paths[2][0,0:3]),
                3: path.path_Jump(self.legs[3].path[self.legs[3].currentPos,0:3],rot_paths[3][0,0:3]),
                4: path.path_Jump(self.legs[4].path[self.legs[4].currentPos,0:3],rot_paths[4][0,0:3]),
                5: path.path_Jump(self.legs[5].path[self.legs[5].currentPos,0:3],rot_paths[5][0,0:3])
            }
            self.moveSteps[0] = 1
            N_jump = [np.shape(temp_path[0])[0],
                      np.shape(temp_path[1])[0],
                      np.shape(temp_path[2])[0],
                      np.shape(temp_path[3])[0],
                      np.shape(temp_path[4])[0],
                      np.shape(temp_path[5])[0]]
            for i in range(6):
                prep_paths1[i] = np.append(prep_paths1[i],[self.legs[i].path[self.legs[i].currentPos,0:3]],0)
            for i in range(3):
                prep_paths1[i] = np.append(prep_paths1[i],temp_path[i],0)
                prep_paths1[i+3] = np.append(prep_paths1[i+3],temp_path[i+3],0)
                for j in range(6):
                    if N_jump[i] > N_jump[i+3]:
                        last_pos = prep_paths1[j][np.shape(prep_paths1[j])[0]-1,0:3]
                        if j == i+3:
                            for k in range(N_jump[i] - N_jump[i+3]):
                                prep_paths1[j] = np.append(prep_paths1[j],[last_pos],0)
                        elif j != i:
                            for k in range(N_jump[i]):
                                prep_paths1[j] = np.append(prep_paths1[j],[last_pos],0)
                    else:
                        last_pos = prep_paths1[j][np.shape(prep_paths1[j])[0]-1,0:3]
                        if j == i:
                            for k in range(N_jump[i+3] - N_jump[i]):
                                prep_paths1[j] = np.append(prep_paths1[j],[last_pos],0)
                        elif j != i+3:
                            for k in range(N_jump[i+3]):
                                prep_paths1[j] = np.append(prep_paths1[j],[last_pos],0)
            self.moveSteps[0] += np.sum([np.max([N_jump[0],N_jump[3]]),np.max([N_jump[1],N_jump[4]]),np.max([N_jump[2],N_jump[5]])])
        #Linear Move
        s = np.sqrt(pow(x - self.zeta[0],2) + pow(y - self.zeta[1],2))
        N = int(np.ceil(s/self.dx))
        self.moveSteps[3] = N 
        if N != 0:
            for i in range(6):
                delayed_path = path.delay(path.path_F, delays[i])
                pathLength = np.shape(delayed_path)[0]
                #Move Legs
                temp_path = np.array([delayed_path[0,0:3]])
                for j in range(N):
                    temp_path = np.append(temp_path, [delayed_path[(j+1)%pathLength,0:3]], 0)
                if i==0 or i==5: temp_path = path.translate(temp_path,[self.pathOffsets[0],self.pathOffsets[1],0])
                elif i==2 or i==3: temp_path = path.translate(temp_path,[-self.pathOffsets[0],self.pathOffsets[1],0])
                lin_paths[i] = path.rotate(temp_path if i<3 else path.reflect(temp_path,1), np.pi*(2*i + 1)/6)
        #Prep Legs For Linear Move
        if self.moveSteps[1] > 0:
            temp_path = {
                0: path.path_Jump(rot_paths[0][self.moveSteps[1],0:3],lin_paths[0][0,0:3]),
                1: path.path_Jump(rot_paths[1][self.moveSteps[1],0:3],lin_paths[1][0,0:3]),
                2: path.path_Jump(rot_paths[2][self.moveSteps[1],0:3],lin_paths[2][0,0:3]),
                3: path.path_Jump(rot_paths[3][self.moveSteps[1],0:3],lin_paths[3][0,0:3]),
                4: path.path_Jump(rot_paths[4][self.moveSteps[1],0:3],lin_paths[4][0,0:3]),
                5: path.path_Jump(rot_paths[5][self.moveSteps[1],0:3],lin_paths[5][0,0:3])
            }
            for i in range(6):
                prep_paths2[i] = np.append(prep_paths2[i],[rot_paths[i][self.moveSteps[1],0:3]],0)
            self.moveSteps[2] = 2
        else:
            temp_path = {
                0: path.path_Jump(self.legs[0].path[self.legs[0].currentPos,0:3],lin_paths[0][0,0:3]),
                1: path.path_Jump(self.legs[1].path[self.legs[1].currentPos,0:3],lin_paths[1][0,0:3]),
                2: path.path_Jump(self.legs[2].path[self.legs[2].currentPos,0:3],lin_paths[2][0,0:3]),
                3: path.path_Jump(self.legs[3].path[self.legs[3].currentPos,0:3],lin_paths[3][0,0:3]),
                4: path.path_Jump(self.legs[4].path[self.legs[4].currentPos,0:3],lin_paths[4][0,0:3]),
                5: path.path_Jump(self.legs[5].path[self.legs[5].currentPos,0:3],lin_paths[5][0,0:3])
            }
            for i in range(6):
                prep_paths2[i] = np.append(prep_paths2[i],[self.legs[i].path[self.legs[i].currentPos,0:3]],0)
                self.moveSteps[2] = 1
        N_jump = [np.shape(temp_path[0])[0],
                  np.shape(temp_path[1])[0],
                  np.shape(temp_path[2])[0],
                  np.shape(temp_path[3])[0],
                  np.shape(temp_path[4])[0],
                  np.shape(temp_path[5])[0]]
        
        for i in range(3):
            prep_paths2[i] = np.append(prep_paths2[i],temp_path[i],0)
            prep_paths2[i+3] = np.append(prep_paths2[i+3],temp_path[i+3],0)
            for j in range(6):
                if N_jump[i] > N_jump[i+3]:
                    last_pos = prep_paths2[j][np.shape(prep_paths2[j])[0]-1,0:3]
                    if j == i+3:
                        for k in range(N_jump[i] - N_jump[i+3]):
                            prep_paths2[j] = np.append(prep_paths2[j],[last_pos],0)
                    elif j != i:
                        for k in range(N_jump[i]):
                            prep_paths2[j] = np.append(prep_paths2[j],[last_pos],0)
                else:
                    last_pos = prep_paths2[j][np.shape(prep_paths2[j])[0]-1,0:3]
                    if j == i:
                        for k in range(N_jump[i+3] - N_jump[i]):
                            prep_paths2[j] = np.append(prep_paths2[j],[last_pos],0)
                    elif j != i+3:
                        for k in range(N_jump[i+3]):
                            prep_paths2[j] = np.append(prep_paths2[j],[last_pos],0)
        self.moveSteps[2] += np.sum([np.max([N_jump[0],N_jump[3]]),np.max([N_jump[1],N_jump[4]]),np.max([N_jump[2],N_jump[5]])])

        #Reset Legs After
        if RESET_AFTER:
            reset_paths = {
                0: np.empty((0,3)),
                1: np.empty((0,3)),
                2: np.empty((0,3)),
                3: np.empty((0,3)),
                4: np.empty((0,3)),
                5: np.empty((0,3)),
            }   
            temp_path = {
                0: path.path_Jump(lin_paths[0][self.moveSteps[3],0:3],[0.1,0,-0.17]),
                1: path.path_Jump(lin_paths[1][self.moveSteps[3],0:3],[0.1,0,-0.17]),
                2: path.path_Jump(lin_paths[2][self.moveSteps[3],0:3],[0.1,0,-0.17]),
                3: path.path_Jump(lin_paths[3][self.moveSteps[3],0:3],[0.1,0,-0.17]),
                4: path.path_Jump(lin_paths[4][self.moveSteps[3],0:3],[0.1,0,-0.17]),
                5: path.path_Jump(lin_paths[5][self.moveSteps[3],0:3],[0.1,0,-0.17])
            }
            for i in range(6):
                reset_paths[i] = np.append(reset_paths[i],[lin_paths[i][self.moveSteps[3],0:3]],0)

            N_jump = [np.shape(temp_path[0])[0],
                      np.shape(temp_path[1])[0],
                      np.shape(temp_path[2])[0],
                      np.shape(temp_path[3])[0],
                      np.shape(temp_path[4])[0],
                      np.shape(temp_path[5])[0]]
        
            for i in range(3):
                reset_paths[i] = np.append(reset_paths[i],temp_path[i],0)
                reset_paths[i+3] = np.append(reset_paths[i+3],temp_path[i+3],0)
                for j in range(6):
                    if N_jump[i] > N_jump[i+3]:
                        last_pos = reset_paths[j][np.shape(reset_paths[j])[0]-1,0:3]
                        if j == i+3:
                            for k in range(N_jump[i] - N_jump[i+3]):
                                reset_paths[j] = np.append(reset_paths[j],[last_pos],0)
                        elif j != i:
                            for k in range(N_jump[i]):
                                reset_paths[j] = np.append(reset_paths[j],[last_pos],0)
                    else:
                        last_pos = reset_paths[j][np.shape(reset_paths[j])[0]-1,0:3]
                        if j == i:
                            for k in range(N_jump[i+3] - N_jump[i]):
                                reset_paths[j] = np.append(reset_paths[j],[last_pos],0)
                        elif j != i+3:
                            for k in range(N_jump[i+3]):
                                reset_paths[j] = np.append(reset_paths[j],[last_pos],0)
            #Combine All the Paths
            for i in range(6): self.legs[i].changePath(np.append(prep_paths1[i],
                                                        np.append(rot_paths[i],
                                                            np.append(prep_paths2[i],
                                                                np.append(lin_paths[i],reset_paths[i],0),0),0),0))
        else:
            #Combine All the Paths
            for i in range(6): self.legs[i].changePath(np.append(prep_paths1[i],
                                                        np.append(rot_paths[i],
                                                            np.append(prep_paths2[i],lin_paths[i],0),0),0))
        #print(self.moveSteps)
        self.totalPathLength = self.legs[0].pathLength


            
class leg:
    def __init__ (self, index, DH, path=np.array([[0.1,0,-0.17]]), offset=[0, 0, np.pi/2]):
        self.a0, self.a1, self.a2, self.a3 = DH[0,0], DH[1,0], DH[2,0], DH[3,0]  #nx3 np array with a, alpha, and d DH parameters
        self.offset = offset
        self.index = index

        self.path = np.copy(path)
        #print(path)
        self.pathLength = np.shape(self.path)[0]
        self.home = self.path[0,0:3]

        self.theta = np.zeros((self.pathLength, 3)) #Servo Angles
        for i in range(self.pathLength): self.theta[i,0:3] = self.IK(self.path[i,0:3])

        self.simulation = np.zeros((4,3)) #Leg servo position data
        self.resetPos()
    
    def changePath(self,path):
        self.path = np.copy(path)
        self.pathLength = np.shape(self.path)[0]
        self.theta = np.zeros((self.pathLength, 3))
        for i in range(self.pathLength): self.theta[i,0:3] = self.IK(self.path[i,0:3])
        self.resetPos()

    def nextPos (self):
        self.currentPos += 1
        if self.currentPos >= self.pathLength: 
            self.currentPos -= 1; return -1
            #self.currentPos = 0
        self.updateSim()
        return 0
        
    def resetPos (self):
        self.currentPos = 0;
        self.updateSim()

    def updateSim (self):
        global SIMULATION
        if not SIMULATION: return
        theta = np.round(self.theta[self.currentPos,0:3] + self.offset,6)#%(3.141593)
        #print(theta)
        self.simulation = np.array([[0,0,0],
                                    [self.a1*np.cos(theta[0]),
                                     self.a1*np.sin(theta[0]),
                                     0],
                                    [(self.a1+self.a2*np.cos(theta[1]))*np.cos(theta[0]),
                                     (self.a1+self.a2*np.cos(theta[1]))*np.sin(theta[0]),
                                     -self.a2*np.sin(theta[1])],
                                    [np.cos(theta[0])*(self.a1+self.a3*np.cos(theta[1]+theta[2])+self.a2*np.cos(theta[1])),
                                     np.sin(theta[0])*(self.a1+self.a3*np.cos(theta[1]+theta[2])+self.a2*np.cos(theta[1])),
                                     -self.a3*np.sin(theta[1]+theta[2])-self.a2*np.sin(theta[1])]])
        #Translate from leg frame to Body frame
        gamma = np.pi*(2*self.index - 1)/6
        R_B0 = np.array([[np.cos(gamma),-np.sin(gamma),0],
                         [np.sin(gamma),np.cos(gamma),0],
                         [0,0,1]])
        for i in range(4):
            self.simulation[i,0:3] = np.transpose(np.dot(R_B0, np.transpose(self.simulation[i,0:3]+[self.a0,0,0])))
        #print(self.simulation)

    def IK (self, P_goal):
        tol = 0.0001 #tolerance for IK
        x, y, z = P_goal[0], P_goal[1], P_goal[2]

        a = (pow(z,2)+pow(np.sqrt(pow(x,2)+pow(y,2))-self.a1,2)-pow(self.a2,2)-pow(self.a3,2))/(2*self.a2*self.a3)
        if pow(a,2) > 1: 
            print("Goal <", x, ", ", y, ", ", z, "> outside workspace!!!") 
            exit(-1)
        psi_3 = np.array([np.arctan2(np.sqrt(1-pow(a,2)),a),
                          np.arctan2(-np.sqrt(1-pow(a,2)),a)])
        #print(psi_3)

        b = [pow((self.a3*np.sin(psi_3[0])),2)+pow((self.a2+self.a3*np.cos(psi_3[0])),2)-pow(z,2),
             pow((self.a3*np.sin(psi_3[1])),2)+pow((self.a2+self.a3*np.cos(psi_3[1])),2)-pow(z,2)]
        psi_2 = []
        if b[0] >= 0: 
            psi_2.append(np.arctan2(np.sqrt(b[0]),-z)+np.arctan2(self.a2+self.a3*np.cos(psi_3[0]),self.a3*np.sin(psi_3[0])))
            psi_2.append(-np.arctan2(np.sqrt(b[0]),-z)+np.arctan2(self.a2+self.a3*np.cos(psi_3[0]),self.a3*np.sin(psi_3[0])))
        if b[1] >= 0:
            psi_2.append(np.arctan2(np.sqrt(b[1]),-z)+np.arctan2(self.a2+self.a3*np.cos(psi_3[1]),self.a3*np.sin(psi_3[1])))
            psi_2.append(-np.arctan2(np.sqrt(b[1]),-z)+np.arctan2(self.a2+self.a3*np.cos(psi_3[1]),self.a3*np.sin(psi_3[1])))
        if len(psi_2) == 0:
            print("Goal <", x, ", ", y, ", ", z, "> outside workspace!!!") 
            exit(-1)
        #print(psi_2)

        c = np.array([self.a3*np.cos(psi_2[0]+psi_3[0])+self.a2*np.cos(psi_2[0])+self.a1,
                      self.a3*np.cos(psi_2[1]+psi_3[0])+self.a2*np.cos(psi_2[1])+self.a1,
                      self.a3*np.cos(psi_2[2]+psi_3[1])+self.a2*np.cos(psi_2[2])+self.a1,
                      self.a3*np.cos(psi_2[3]+psi_3[1])+self.a2*np.cos(psi_2[3])+self.a1])
        psi_1 = np.array([np.arctan2(y/c[0],x/c[0]),
                          np.arctan2(y/c[1],x/c[1]),
                          np.arctan2(y/c[2],x/c[2]),
                          np.arctan2(y/c[3],x/c[3])])
        #print(psi_1)
        for i in range(4):
            #print(np.cos(psi_1[i])*(self.a1+self.a3*np.cos(psi_2[i]+psi_3[int(i/2)])+self.a2*np.cos(psi_2[i])))
            #print(np.sin(psi_1[i])*(self.a1+self.a3*np.cos(psi_2[i]+psi_3[int(i/2)])+self.a2*np.cos(psi_2[i])))
            #print(-self.a3*np.sin(psi_2[i]+psi_3[int(i/2)])-self.a2*np.sin(psi_2[i]))
            if psi_3[int(i/2)] - self.offset[2] > np.pi/2 or psi_3[int(i/2)] - self.offset[2] < -np.pi/2: continue
            if psi_1[i] - self.offset[0] > np.pi/2 or psi_1[i] - self.offset[0] < -np.pi/2: continue
            if psi_2[i] - self.offset[1] > np.pi/2 or psi_2[i] - self.offset[1] < -np.pi/2: continue
            if (x+tol < np.cos(psi_1[i])*(self.a1+self.a3*np.cos(psi_2[i]+psi_3[int(i/2)])+self.a2*np.cos(psi_2[i]))) or (x-tol > np.cos(psi_1[i])*(self.a1+self.a3*np.cos(psi_2[i]+psi_3[int(i/2)])+self.a2*np.cos(psi_2[i]))) or\
               (y+tol < np.sin(psi_1[i])*(self.a1+self.a3*np.cos(psi_2[i]+psi_3[int(i/2)])+self.a2*np.cos(psi_2[i]))) or (y-tol > np.sin(psi_1[i])*(self.a1+self.a3*np.cos(psi_2[i]+psi_3[int(i/2)])+self.a2*np.cos(psi_2[i]))) or\
               (z+tol < -self.a3*np.sin(psi_2[i]+psi_3[int(i/2)])-self.a2*np.sin(psi_2[i])) or (z-tol > -self.a3*np.sin(psi_2[i]+psi_3[int(i/2)])-self.a2*np.sin(psi_2[i])):  
                continue
            return np.round(np.array([psi_1[i], psi_2[i], psi_3[int(i/2)]]) - self.offset,6)
        
        print("Goal <", x, ", ", y, ", ", z, "> outside workspace!!!")
        exit(-1)
