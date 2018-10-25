from __future__ import print_function, absolute_import, division
import time
import sys
import math
from api import vrep


class PID:

    def __init__(self, dt, Kp=0, Ki=0, Kd=0):

        self.dt = dt
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.reset()

    def Gain(self, err):

        if type(self.err_p) = type(None):
            self.err_p = err
        self.errsum += err*dt
        d_err = (err-self.err_p)/dt
        self.d_err = err

        return self.Kp*err+self.Ki*errsum+self.Kd*d_err

    def reset(self):
        self.err_p = None
        self.errsum = 0.0



if __name__=='__main__':
    try:
        vrep.simxFinish(-1) # just in case, close all opened connections
    except:
        pass

    opmode_blocking = vrep.simx_opmode_blocking

    clientID=vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5) # Connect to V-REP

    if clientID != -1:
        print('Connected to remote API server')

        # enable the synchronous mode on the client:
        vrep.simxSynchronous(clientID, True)

        # get joint handles:
        joint_handle = [
            vrep.simxGetObjectHandle(clientID, 'MTB_axis1', opmode_blocking)[1],
            vrep.simxGetObjectHandle(clientID, 'MTB_axis2', opmode_blocking)[1]
        ]

        # get target handle
        cube_handle = vrep.simxGetObjectHandle(clientID, 'Cube', opmode_blocking)[1]

        # link length
        a1 = 0.467
        a2 = 0.4

        # start the simulation:
        vrep.simxStartSimulation(clientID,vrep.simx_opmode_blocking)
        vrep.simxSynchronousTrigger(clientID)

        # desired pose
        [x_d, y_d, _] = vrep.simxGetObjectPosition(clientID, cube_handle, -1, opmode_blocking)[1]

        # desired joint angle
        j2_d = math.acos(x_d-

        j1_d = 
        j2_d = x

        # Now step a few times:
        for i in range(1,100):
            vrep.simxSynchronousTrigger(clientID)

        # stop the simulation:
        vrep.simxStopSimulation(clientID,vrep.simx_opmode_blocking)

        # Now close the connection to V-REP:
        vrep.simxFinish(clientID)
    else:
        print ('Failed connecting to remote API server')
    print ('Program ended')

