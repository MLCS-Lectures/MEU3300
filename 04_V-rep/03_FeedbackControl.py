from __future__ import print_function, absolute_import, division
import time
import sys
import math
from api import vrep


class PID:

    def __init__(self, dt=0.05, Kp=0, Ki=0, Kd=0):

        self.dt = dt
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.reset()

    def feedback(self, err):

        if type(self.err_p) == type(None):
            self.err_p = err
        self.errsum += err*self.dt
        d_err = (err-self.err_p)/self.dt
        self.err_p = err

        return self.Kp*err+self.Ki*self.errsum+self.Kd*d_err

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
        a2 = 0.405

        # start the simulation:
        vrep.simxStartSimulation(clientID,vrep.simx_opmode_blocking)
        vrep.simxSynchronousTrigger(clientID)

        # desired pose of end-effector
        x_d, y_d, z_d = vrep.simxGetObjectPosition(clientID, cube_handle, -1, opmode_blocking)[1]

        # get desired joint angle
        d_square = x_d**2+y_d**2
        d = math.sqrt(d_square)
        if d > a1+a2 or d < a1-a2: # solutions are in the complex domain
            j1_d, j2_d = [0.0, 0.0]
            print('Not in reachable workspace.')
        else:
            cos_j2_d = (d_square-a1**2-a2**2)/2.0/a1/a2
            j2_d = math.acos(cos_j2_d)
            j2_d *= -1 if y_d < 0 else 1 # there's two solutions, so we have to choose the optimal one
            j1_d = math.atan2(y_d, x_d)-math.atan2(a2*math.sin(j2_d), a1+a2*cos_j2_d)
        
        # import PID controller object
        pid_j1 = PID(dt=0.05, Kp=3.0, Ki=0.0, Kd=0.5)
        pid_j2 = PID(dt=0.05, Kp=1.5, Ki=0.001, Kd=0.0)

        # Now step a few times:
        for t in range(1,200):
            vrep.simxSynchronousTrigger(clientID)

            # current joint angle
            j1 = vrep.simxGetJointPosition(clientID, joint_handle[0],opmode_blocking)[1]
            j2 = vrep.simxGetJointPosition(clientID, joint_handle[1],opmode_blocking)[1]

            # control input from PID
            u1 = pid_j1.feedback(j1_d-j1)
            u2 = pid_j2.feedback(j2_d-j2)
            
            # apply control input to the actuators
            vrep.simxSetJointTargetVelocity(clientID, joint_handle[0], u1, opmode_blocking)
            vrep.simxSetJointTargetVelocity(clientID, joint_handle[1], u2, opmode_blocking)

        # stop the simulation:
        vrep.simxStopSimulation(clientID,vrep.simx_opmode_blocking)

        # Now close the connection to V-REP:
        vrep.simxFinish(clientID)
    else:
        print ('Failed connecting to remote API server')
    print ('Program ended')

