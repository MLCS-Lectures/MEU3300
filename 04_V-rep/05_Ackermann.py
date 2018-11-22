from __future__ import print_function, absolute_import, division
import time
import sys
import math
import numpy as np
from api import vrep

# Vehicle geometry
L = 2.2      # distance between front and rear wheel
w = 1.44     # distance between left and right wheel
d = 0.63407  # wheel diameter

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
            vrep.simxGetObjectHandle(clientID, 'steeringLeft', opmode_blocking)[1],
            vrep.simxGetObjectHandle(clientID, 'steeringRight', opmode_blocking)[1],
            vrep.simxGetObjectHandle(clientID, 'motorLeft', opmode_blocking)[1],
            vrep.simxGetObjectHandle(clientID, 'motorRight', opmode_blocking)[1]
        ]

        # start the simulation:
        vrep.simxStartSimulation(clientID,vrep.simx_opmode_blocking)
        vrep.simxSynchronousTrigger(clientID)

        # Now step a few times:
        for t in range(1,300):
            vrep.simxSynchronousTrigger(clientID)
            
            # control input 
            vel = 10                    # m/s. there's no maximum velocity, but maximum torque is 200 Nm
            delta_ack = np.deg2rad(40)  # rad/s. maximum is 0.698131 (40 degree)
            if t > 150:
                delta_ack *= -1


            # Ackermann steering
            R = L/np.abs(delta_ack)
            delta_o = np.arctan2(L,R+w/2)
            delta_i = np.arctan2(L,R-w/2)
            if delta_ack > 0:
                deltaLeft = delta_i
                deltaRight = delta_o
            elif delta_ack < 0:
                deltaLeft = -delta_o
                deltaRight = -delta_i
            else:
                deltaLeft = 0
                deltaRight = 0

            vrep.simxSetJointTargetPosition(clientID, joint_handle[0], deltaLeft, opmode_blocking)
            vrep.simxSetJointTargetPosition(clientID, joint_handle[1], deltaRight, opmode_blocking)
            vrep.simxSetJointTargetVelocity(clientID, joint_handle[2], 2*vel/d, opmode_blocking)
            vrep.simxSetJointTargetVelocity(clientID, joint_handle[3], 2*vel/d, opmode_blocking)

        # stop the simulation:
        vrep.simxStopSimulation(clientID,vrep.simx_opmode_blocking)

        # Now close the connection to V-REP:
        vrep.simxFinish(clientID)
    else:
        print ('Failed connecting to remote API server')
    print ('Program ended')