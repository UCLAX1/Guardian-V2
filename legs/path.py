import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import legs
import time

##-----------SIMULATION CODE-----------##
class simulation:
	def __init__(self, guardian, ts, frames):
		self.guardian = guardian
		#Define virtual guardian
		self.chassis = np.zeros((7,3))
		self.pathLength = np.shape(self.guardian()[0].path)[0]
		r = self.guardian()[0].a0/np.cos(np.pi/6)
		for i in range(6):
			self.chassis[i,0:3] = [r*np.cos(i*np.pi/3),r*np.sin(i*np.pi/3),0]
		self.chassis[6,0:3] = [r,0,0]
		self.path  = rotate(self.guardian()[0].path,-np.pi/6)
		#Set up figure and plots
		self.fig = plt.figure()
		self.ax1 = self.fig.add_subplot(1,2,1,projection="3d")
		self.ax1.set_xlabel('X'); self.ax1.set_ylabel('Y'); self.ax1.set_zlabel('Z')
		self.ax2 = self.fig.add_subplot(1,2,2,projection="3d")
		self.ax2_lims = [-0.25, 0.25]
		self.ax2.set_xlim3d(self.ax2_lims[0], self.ax2_lims[1])
		self.ax2.set_ylim3d(self.ax2_lims[0], self.ax2_lims[1])
		self.ax2.set_zlim3d(path_F[0,2], path_F[0,2]+2*self.ax2_lims[1])
		self.ax2.set_xlabel('X'); self.ax2.set_ylabel('Y'); self.ax2.set_zlabel('Z')
		#Define lines to plot and define animation loop
		self.trj_graphics = [self.ax1.plot(self.path[0,0], self.path[0,1], self.path[0,2], 'o')[0],
						     self.ax1.plot(self.path[0:self.pathLength,0], 
										   self.path[0:self.pathLength,1], 
										   self.path[0:self.pathLength,2])[0]]
		self.rbt_graphics = [self.ax2.plot(self.guardian()[i].simulation[0:4,0], 
										   self.guardian()[i].simulation[0:4,1], 
										   self.guardian()[i].simulation[0:4,2], 'o-')[0] for i in range(6)]
		self.rbt_graphics.append(self.ax2.plot(np.transpose(self.chassis[0:7,0]), 
											   np.transpose(self.chassis[0:7,1]),
											   np.transpose(self.chassis[0:7,2]))[0])
		self.legAnimation = FuncAnimation(self.fig, self.nextFrame, ts*frames, interval=ts)


	def nextFrame(self,j):
		self.guardian.nextPos()
		for i in range(6):
			temp_leg = translate(rotate(self.guardian()[i].simulation,-self.guardian.zeta[2]),[self.guardian.zeta[0],self.guardian.zeta[1],0])
			self.rbt_graphics[i].set_data(np.transpose(temp_leg[0:4,0:2]))
			self.rbt_graphics[i].set_3d_properties(np.transpose(temp_leg[0:4,2]))
		temp_chassis = translate(rotate(self.chassis,-self.guardian.zeta[2]),[self.guardian.zeta[0],self.guardian.zeta[1],0])
		self.rbt_graphics[6].set_data(np.transpose(temp_chassis[0:7,0:2]))
		self.rbt_graphics[6].set_3d_properties(np.transpose(temp_chassis[0:7,2]))

		self.trj_graphics[0].set_data(self.path[self.guardian()[0].currentPos,0:2])
		self.trj_graphics[0].set_3d_properties(self.path[self.guardian()[0].currentPos,2]) 

		self.ax2.set_xlim3d(self.ax2_lims[0]+self.guardian.zeta[0], self.ax2_lims[1]+self.guardian.zeta[0])
		self.ax2.set_ylim3d(self.ax2_lims[0]+self.guardian.zeta[1], self.ax2_lims[1]+self.guardian.zeta[1])

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

def path_Jump(cur_pos, end_pos):
	new_path = np.array([cur_pos])
	if cur_pos[0] != end_pos[0] or cur_pos[1] != end_pos[1] or cur_pos[2] != end_pos[2]:
		z_high = -0.17+0.031; z_low = -0.17
		N = int(np.ceil(np.abs(cur_pos[2] - z_high)/0.01))
		z_moves = np.linspace(cur_pos[2],z_high,N)
		for i in range(N):
			new_path = np.append(new_path,[[cur_pos[0],cur_pos[1],z_moves[i]]],0)
		N_x = int(np.ceil(np.abs(cur_pos[0] - end_pos[0])/0.01))
		N_y = int(np.ceil(np.abs(cur_pos[1] - end_pos[1])/0.01))
		N = N_x if N_x > N_y else N_y
		x_moves = np.linspace(cur_pos[0],end_pos[0],N)
		y_moves = np.linspace(cur_pos[1],end_pos[1],N)
		for i in range(N):
			new_path = np.append(new_path,[[x_moves[i],y_moves[i],z_high]],0)
		new_path = np.append(new_path,np.array([[end_pos[0],end_pos[1],-0.17+0.026],
												[end_pos[0],end_pos[1],-0.17+0.015],
												[end_pos[0],end_pos[1],-0.17]]),0)
	return new_path


##-----------PATH DEFINITIONS-----------##
#path_F is defined using body unit vectors but using the origin of leg frame 0
#When passed to a leg, the path is interpreted as using leg frame 0 unit vectors, not body unit vectors
path_F = np.array([[0.000000, 0.100000, -0.170000],
				[-0.003750, 0.100000, -0.170000],
				[-0.007500, 0.100000, -0.170000],
				[-0.011250, 0.100000, -0.170000],
				[-0.015000, 0.100000, -0.170000],
				[-0.018750, 0.100000, -0.170000],
				[-0.022500, 0.100000, -0.170000],
				[-0.026250, 0.100000, -0.170000],
				[-0.030000, 0.100000, -0.170000],
				[-0.033750, 0.100000, -0.170000],
				[-0.037500, 0.100000, -0.170000],
				[-0.041250, 0.100000, -0.170000],
				[-0.045000, 0.100000, -0.170000],
				[-0.048750, 0.100000, -0.170000],
				[-0.052500, 0.100000, -0.170000],
				[-0.056250, 0.100000, -0.170000],
				[-0.060000, 0.100000, -0.170000],
				[-0.058847, 0.100000, -0.160245],
				[-0.055433, 0.100000, -0.150866],
				[-0.049888, 0.100000, -0.142221],
				[-0.042426, 0.100000, -0.134645],
				[-0.033334, 0.100000, -0.128427],
				[-0.022961, 0.100000, -0.123806],
				[-0.011705, 0.100000, -0.120961],
				[0.000000, 0.100000, -0.120000],
				[0.011705, 0.100000, -0.120961],
				[0.022961, 0.100000, -0.123806],
				[0.033334, 0.100000, -0.128427],
				[0.042426, 0.100000, -0.134645],
				[0.049888, 0.100000, -0.142221],
				[0.055433, 0.100000, -0.150866],
				[0.058847, 0.100000, -0.160245],
				[0.060000, 0.100000, -0.170000],
				[0.056250, 0.100000, -0.170000],
				[0.052500, 0.100000, -0.170000],
				[0.048750, 0.100000, -0.170000],
				[0.045000, 0.100000, -0.170000],
				[0.041250, 0.100000, -0.170000],
				[0.037500, 0.100000, -0.170000],
				[0.033750, 0.100000, -0.170000],
				[0.030000, 0.100000, -0.170000],
				[0.026250, 0.100000, -0.170000],
				[0.022500, 0.100000, -0.170000],
				[0.018750, 0.100000, -0.170000],
				[0.015000, 0.100000, -0.170000],
				[0.011250, 0.100000, -0.170000],
				[0.007500, 0.100000, -0.170000],
				[0.003750, 0.100000, -0.170000]])
#path_CCW is defined in the leg frame 0 directly
path_CCW = np.array([[0.100000, 0.000000, -0.170000],
				[0.099963, -0.002727, -0.170000],
				[0.099851, -0.005451, -0.170000],
				[0.099666, -0.008172, -0.170000],
				[0.099406, -0.010887, -0.170000],
				[0.099072, -0.013593, -0.170000],
				[0.098664, -0.016290, -0.170000],
				[0.098183, -0.018974, -0.170000],
				[0.097630, -0.021644, -0.170000],
				[0.097003, -0.024298, -0.170000],
				[0.096305, -0.026934, -0.170000],
				[0.095534, -0.029550, -0.170000],
				[0.094693, -0.032144, -0.170000],
				[0.093781, -0.034714, -0.170000],
				[0.092800, -0.037258, -0.170000],
				[0.091749, -0.039775, -0.170000],
				[0.090631, -0.042262, -0.170000],
				[0.090631, -0.041450, -0.160245],
				[0.090631, -0.039045, -0.150866],
				[0.090631, -0.035139, -0.142221],
				[0.090631, -0.029884, -0.134645],
				[0.090631, -0.023479, -0.128427],
				[0.090631, -0.016173, -0.123806],
				[0.090631, -0.008245, -0.120961],
				[0.090631, -0.000000, -0.120000],
				[0.090631, 0.008245, -0.120961],
				[0.090631, 0.016173, -0.123806],
				[0.090631, 0.023479, -0.128427],
				[0.090631, 0.029884, -0.134645],
				[0.090631, 0.035139, -0.142221],
				[0.090631, 0.039045, -0.150866],
				[0.090631, 0.041450, -0.160245],
				[0.090631, 0.042262, -0.170000],
				[0.091749, 0.039775, -0.170000],
				[0.092800, 0.037258, -0.170000],
				[0.093781, 0.034714, -0.170000],
				[0.094693, 0.032144, -0.170000],
				[0.095534, 0.029550, -0.170000],
				[0.096305, 0.026934, -0.170000],
				[0.097003, 0.024298, -0.170000],
				[0.097630, 0.021644, -0.170000],
				[0.098183, 0.018974, -0.170000],
				[0.098664, 0.016290, -0.170000],
				[0.099072, 0.013593, -0.170000],
				[0.099406, 0.010887, -0.170000],
				[0.099666, 0.008172, -0.170000],
				[0.099851, 0.005451, -0.170000],
				[0.099963, 0.002727, -0.170000]])

##-----------MAIN-----------##
if __name__ == '__main__' and legs.SIMULATION:
	guardian = legs.guardian()
	guardian.calculateMoveTrajectory(-1, 0, True)

	#while True:
	#    guardian.nextPos()
	#    time.sleep(0.01)
	sim = simulation(guardian, 10, 50)
	sim.show(); del sim #Nothing after this line will run until plot window is closed
