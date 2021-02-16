import numpy as np

SIMULATION = True

class leg:
    def __init__ (self, index, DH, path=np.array([[.5,0,-1]]), offset=[0, 0, -np.pi/2]):
        self.a0, self.a2, self.a3 = DH[0,0], DH[2,0], DH[3,0]  #nx3 np array with a, alpha, and d DH parameters
        self.offset = offset
        self.index = index

        self.path = np.copy(path)
        self.pathLength = np.shape(self.path)[0]

        self.theta = np.zeros((self.pathLength, 3)) #Servo Angles
        for i in range(self.pathLength): self.theta[i,0:3] = self.IK(self.path[i,0:3])

        self.simulation = np.zeros((3,3)) #Leg servo position data
        self.resetPos()
     
    def changePath(self,path):
        self.path = np.copy(path)
        for i in range(self.pathLength): self.theta[i,0:3] = self.IK(self.path[i,0:3])
        self.resetPos()

    def nextPos (self):
        self.currentPos += 1
        if self.currentPos >= self.pathLength: self.currentPos = 0
        self.updateSim()
        
    def resetPos (self):
        self.currentPos = 0;
        self.updateSim()

    def updateSim (self):
        global SIMULATION
        if not SIMULATION: return
        theta = np.round(self.theta[self.currentPos,0:3] + self.offset,6)#%(3.141593)
        #print(theta)
        self.simulation = np.array([[0,0,0],
                                    [self.a2*np.cos(theta[0])*np.cos(theta[1])
                                     ,self.a2*np.sin(theta[0])*np.cos(theta[1]),
                                     self.a2*np.sin(theta[1])],
                                    [np.cos(theta[0])*(self.a3*np.cos(theta[1]+theta[2])+self.a2*np.cos(theta[1])),
                                     np.sin(theta[0])*(self.a3*np.cos(theta[1]+theta[2])+self.a2*np.cos(theta[1])),
                                     self.a3*np.sin(theta[1]+theta[2])+self.a2*np.sin(theta[1])]])
        #Translate from leg frame to Body frame
        gamma = np.pi*(2*self.index - 1)/6
        R_B0 = np.array([[np.cos(gamma),-np.sin(gamma),0],
                         [np.sin(gamma),np.cos(gamma),0],
                         [0,0,1]])
        for i in range(3):
            self.simulation[i,0:3] = np.transpose(np.dot(R_B0, np.transpose(self.simulation[i,0:3]+[self.a0,0,0])))
        #print(self.simulation)

    def IK (self, P_goal):
        tol = 0.0001 #tolerance for IK
        x, y, z = P_goal[0], P_goal[1], P_goal[2]

        a = (pow(x,2)+pow(y,2)+pow(z,2)-pow(self.a2,2)-pow(self.a3,2))/(2*self.a2*self.a3)
        if pow(a,2) > 1: 
            print("Goal <", x, ", ", y, ", ", z, "> outside workspace!!!") 
            exit(-1)
        psi_3 = np.array([np.arctan2(np.sqrt(1-pow(a,2)),a),
                          np.arctan2(-np.sqrt(1-pow(a,2)),a)])
        #print(psi_3)
        if (-1 <= np.sin(psi_3[0] - self.offset[2])) and (np.sin(psi_3[0] - self.offset[2]) <= 1): psi_3 = psi_3[0]
        elif (-1 <= np.sin(psi_3[1] - self.offset[2])) and (np.sin(psi_3[1] - self.offset[2]) <= 1): psi_3 = psi_3[1]
        else: print("psi_3 inverse kinematics error")

        b = pow((self.a3*np.sin(psi_3)),2)+pow((self.a2+self.a3*np.cos(psi_3)),2)-pow(z,2)
        if b < 0: 
            print("Goal <", x, ", ", y, ", ", z, "> outside workspace!!!") 
            exit(-1)
        psi_2 = np.array([np.arctan2(np.sqrt(b),z)+np.arctan2(self.a2+self.a3*np.cos(psi_3),self.a3*np.sin(psi_3)),
                          np.arctan2(-np.sqrt(b),z)+np.arctan2(self.a2+self.a3*np.cos(psi_3),self.a3*np.sin(psi_3))])
        #print(psi_2)
        if (-1 <= np.sin(psi_2[0] - self.offset[1])) and (np.sin(psi_2[0] - self.offset[1]) <= 1): psi_2 = psi_2[0]
        elif (-1 <= np.sin(psi_2[1] - self.offset[1])) and (np.sin(psi_2[1] - self.offset[1]) <= 1): psi_2 = psi_2[1]
        else: print("psi_2 inverse kinematics error")

        c = self.a3*np.cos(psi_2+psi_3)+self.a2*np.cos(psi_2)
        psi_1 = np.arctan2(y/c,x/c)
        #print(psi_1)
        if (-1 > np.sin(psi_1 - self.offset[0])) or (np.sin(psi_1 - self.offset[0]) > 1): print("psi_1 inverse kinematics error") 
        #print(np.cos(psi_1)*(self.a3*np.cos(psi_2+psi_3)+self.a2*np.cos(psi_2)))
        #print(np.sin(psi_1)*(self.a3*np.cos(psi_2+psi_3)+self.a2*np.cos(psi_2)))
        #print(self.a3*np.sin(psi_2+psi_3)+self.a2*np.sin(psi_2))
        if (x+tol < np.cos(psi_1)*(self.a3*np.cos(psi_2+psi_3)+self.a2*np.cos(psi_2))) or (x-tol > np.cos(psi_1)*(self.a3*np.cos(psi_2+psi_3)+self.a2*np.cos(psi_2))) or\
           (y+tol < np.sin(psi_1)*(self.a3*np.cos(psi_2+psi_3)+self.a2*np.cos(psi_2))) or (y-tol > np.sin(psi_1)*(self.a3*np.cos(psi_2+psi_3)+self.a2*np.cos(psi_2))) or\
           (z+tol < self.a3*np.sin(psi_2+psi_3)+self.a2*np.sin(psi_2)) or (z-tol > self.a3*np.sin(psi_2+psi_3)+self.a2*np.sin(psi_2)):
                print("Goal <", x, ", ", y, ", ", z, "> outside workspace!!!")
                exit(-1)
        return np.round(np.array([psi_1, psi_2, psi_3]) - self.offset,6)



##-----------MAIN-----------##
if __name__ == '__main__':
    DH = np.array([[0,0,0],
                   [0,-np.pi/2, 0],
                   [0.5,0,0],
                   [1,0,0]])
    l = leg(1, DH)
