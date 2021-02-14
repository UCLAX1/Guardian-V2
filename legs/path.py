import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import legs

path = np.array([[.5,0,-1],
				 [.5,0.15,-1],
				 [.5,0.3,-1],
				 [.5,0.45,-1],
				 [.5,0.6,-.5],
				 
				 [.5,0.3,-.5],
				 [.5,0,-.5],
				 [.5,-0.3,-.5],

				 [.5,-0.6,-.5],
				 [.5,-0.45,-1],
				 [.5,-0.3,-1],
				 [.5,-0.15,-1]])

DH = np.array([[0,0,0],
                   [0,-np.pi/2, 0],
                   [0.5,0,0],
                   [1,0,0]])
l = legs.leg(DH,path)

fig = plt.figure()
ax = fig.add_subplot(projection="3d")
r = l.a2+l.a3
ax.set_xlim3d(-.75, .75)
ax.set_ylim3d(-.75, .75)
ax.set_zlim3d(-1, .5)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

#ax.plot([1, 2, 3, 4], [1, 4, 2, 3], [5,3,2,0])
lines = [ax.plot(l.simulation[0:3,0], l.simulation[0:3,1], l.simulation[0:3,2], 'o-')[0],
		 ax.plot(l.path[0,0], l.path[0,1], l.path[0,2], 'o')[0]]


def animate_path(i):
	length = np.shape(path)[0]
	line_path.set_data(path[i%length,0:2])
	line_path.set_3d_properties(path[i%length,2]) 
	return line_path 

def animate(i):
	l.nextPos()
	lines[0].set_data(np.transpose(l.simulation[0:3,0:2]))
	lines[0].set_3d_properties(np.transpose(l.simulation[0:3,2])) 

	lines[1].set_data(l.path[l.currentPos,0:2])
	lines[1].set_3d_properties(l.path[l.currentPos,2]) 

	return lines

ts, frames = 250, 50
legAnimation = FuncAnimation(fig, animate, ts*frames, interval=ts)
#pathAnimation = FuncAnimation(fig, animate_path, ts*frames, interval=ts)
plt.show()