import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import legs

##-----------SIMULATION CODE-----------##
class simulation:
	def __init__(self, guardian, ts, frames):
		#Define virtual guardian
		self.guardian = guardian
		self.chassis = np.zeros((7,3))
		self.pathLength = np.shape(guardian[0].path)[0]
		r = guardian[0].a0/np.cos(np.pi/6)
		for i in range(6):
			self.chassis[i,0:3] = [r*np.cos(i*np.pi/3),r*np.sin(i*np.pi/3),0]
		self.chassis[6,0:3] = [r,0,0]
		self.path  = rotate(guardian[0].path,-np.pi/6)
		#Set up figure and plots
		self.fig = plt.figure()
		self.ax1 = self.fig.add_subplot(1,2,1,projection="3d")
		self.ax1.set_xlabel('X'); self.ax1.set_ylabel('Y'); self.ax1.set_zlabel('Z')
		self.ax2 = self.fig.add_subplot(1,2,2,projection="3d")
		self.ax2.set_xlim3d(-1.25, 1.25)
		self.ax2.set_ylim3d(-1.25, 1.25)
		self.ax2.set_zlim3d(-1.25, 1.25)
		self.ax2.set_xlabel('X'); self.ax2.set_ylabel('Y'); self.ax2.set_zlabel('Z')
		#Define lines to plot and define animation loop
		self.lines1 = [self.ax1.plot(self.path[2,0], self.path[2,1], self.path[2,2], 'o')[0],
					   self.ax1.plot(np.append(np.transpose(self.path[0:self.pathLength,0]),self.path[0,0]), 
									 np.append(np.transpose(self.path[0:self.pathLength,1]),self.path[0,1]), 
									 np.append(np.transpose(self.path[0:self.pathLength,2]),self.path[0,2]))[0]]
		self.lines2 = [self.ax2.plot(self.guardian[i].simulation[0:3,0], self.guardian[i].simulation[0:3,1], self.guardian[i].simulation[0:3,2], 'o-')[0] for i in range(6)]
		self.lines2.append(self.ax2.plot(np.transpose(self.chassis[0:7,0]), np.transpose(self.chassis[0:7,1]), np.transpose(self.chassis[0:7,2]))[0])
		self.legAnimation = FuncAnimation(self.fig, self.nextFrame, ts*frames, interval=ts)

	def nextFrame(self,j):
		for i in range(6):
			self.guardian[i].nextPos()
			self.lines2[i].set_data(np.transpose(self.guardian[i].simulation[0:3,0:2]))
			self.lines2[i].set_3d_properties(np.transpose(self.guardian[i].simulation[0:3,2]))
		self.lines1[0].set_data(self.path[self.guardian[0].currentPos,0:2])
		self.lines1[0].set_3d_properties(self.path[self.guardian[0].currentPos,2]) 
		return [self.lines1, self.lines2]

	def show(self):
		plt.show()


##-----------PATH HELPER FUNCTIONS-----------##
def reflect(path, axis):
	if axis < 0 or axis > 2: return -1
	new_path = np.copy(path)
	for i in range(np.shape(path)[0]): new_path[i,axis] = -new_path[i,axis]
	return new_path
def delay(path, index_delay):
	return np.roll(path, -index_delay, 0)
def translate(path, P = [0,0,0]):
	return path + P
def rotate(path, gamma):
	Rz = np.array([[np.cos(gamma),np.sin(gamma),0],
				   [-np.sin(gamma),np.cos(gamma),0],
			   	   [0,0,1]])
	new_path = np.copy(path)
	for i in range(np.shape(path)[0]):
		new_path[i,0:3] = np.transpose(np.dot(Rz, np.transpose(path[i,0:3])))
	return new_path


##-----------PATH DEFINITIONS-----------##
#Paths are defined below using body unit vectors but using the origin of leg frame 0
#When passed to a leg, the path is interpreted as using leg frame 0 unit vectors not body unit vectors
path_F = np.array([[0,0.6,-1],
				   [-0.05,0.6,-1],
				   [-0.1,0.6,-1],
				   [-0.15,0.6,-1],
				   [-0.2,0.6,-1],
				   [-0.25,0.6,-1],
				   [-0.3,0.6,-1],
				   [-0.35,0.6,-1],
				   [-0.4,0.6,-1],
				   
				   [-0.3,0.6,-.75],
				   [-0.2,0.6,-.67],
				   [-0.1,0.6,-.62],
				   [0,0.6,-.6],
				   [0.1,0.6,-.62],
				   [0.2,0.6,-.67],
				   [0.3,0.6,-.75],
				   
				   [0.4,0.6,-1],
				   [0.35,0.6,-1],
				   [0.3,0.6,-1],
				   [0.25,0.6,-1],
				   [0.2,0.6,-1],
				   [0.15,0.6,-1],
				   [0.1,0.6,-1],
				   [0.05,0.6,-1]])

path_CCW = np.array([[0.6,0,-1],
					 [0.6,-0.05,-1],
					 [0.6,-0.1,-1],
					 [0.6,-0.15,-1],
					 [0.6,-0.2,-1],
					 [0.6,-0.25,-1],
					 [0.6,-0.3,-1],
					 [0.6,-0.35,-1],
					 [0.6,-0.4,-1],
					 
					 [0.6,-0.3,-.75],
					 [0.6,-0.2,-.67],
					 [0.6,-0.1,-.62],
					 [0.6,0,-.6],
					 [0.6,0.1,-.62],
					 [0.6,0.2,-.67],
					 [0.6,0.3,-.75],
					 
					 [0.6,0.4,-1],
					 [0.6,0.35,-1],
					 [0.6,0.3,-1],
					 [0.6,0.25,-1],
					 [0.6,0.2,-1],
					 [0.6,0.15,-1],
					 [0.6,0.1,-1],
					 [0.6,0.05,-1]])


##-----------MAIN-----------##
if __name__ == '__main__' and legs.SIMULATION:
	DH = np.array([[0.6,0,0],
				   [0,-np.pi/2, 0],
				   [0.6,0,0],
				   [0.9,0,0]])
	guardian = []

	print("Simulating Forward Gait")
	for i in range(6):
		temp_path = np.copy(path_F)
		if i==0 or i==5: temp_path = translate(temp_path,[0.3,-0.1,0])
		elif i==2 or i==3: temp_path = translate(temp_path,[-0.3,-0.1,0])
		guardian.append(legs.leg(i+1,DH,delay(rotate(temp_path if i<3 else reflect(temp_path,1), np.pi*(2*i + 1)/6), (i%3)*8)))
	sim = simulation(guardian, 80, 50)
	sim.show(); del sim #Nothing after this line will run until plot window is closed
	print("Simulating Reverse Rotation Gait")
	for i in range(6):
		temp_path = reflect(path_F,0)
		if i==0 or i==5: temp_path = translate(temp_path,[0.3,-0.1,0])
		elif i==2 or i==3: temp_path = translate(temp_path,[-0.3,-0.1,0])
		guardian[i].changePath(delay(rotate(temp_path if i<3 else reflect(temp_path,1), np.pi*(2*i + 1)/6), (i%3)*8))
	sim = simulation(guardian, 80, 50)
	sim.show(); del sim  #Nothing after this line will run until plot window is closed

	print("Simulating CCW Rotation Gait")
	for i in range(6): guardian[i].changePath(delay(path_CCW,int(i*np.shape(path_CCW)[0]/6)))
	sim = simulation(guardian, 80, 50)
	sim.show(); del sim  #Nothing after this line will run until plot window is closed
	print("Simulating CW Rotation Gait")
	for i in range(6): guardian[i].changePath(delay(reflect(path_CCW,1),int(i*np.shape(path_CCW)[0]/6)))
	sim = simulation(guardian, 80, 50)
	sim.show(); del sim  #Nothing after this line will run until plot window is closed
