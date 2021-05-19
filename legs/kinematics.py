import numpy as np

def T_Matrix (alpha, a, theta, d, offset):
    theta = theta*np.pi/180
    return np.array([
        [np.cos(theta), -np.sin(theta), 0, a],
        [np.sin(theta)*np.cos(alpha), np.cos(theta)*np.cos(alpha), -np.sin(alpha), -np.sin(alpha)*d],
        [np.sin(theta)*np.sin(alpha), np.cos(theta)*np.sin(alpha), np.cos(alpha), np.cos(alpha)*d],
        [0, 0, 0, 1]])

def quanticSolve ():
    pass

if __name__ == '__main__':
    t = 90
    print(T_Matrix(0,0,t,0,0))