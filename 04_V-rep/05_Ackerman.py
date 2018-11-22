from __future__ import print_function, absolute_import, division
import time
import sys
import math
import numpy as np
from api import vrep

L = 2.2
w = 1.44

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

        # get target handle
        robot_handle = vrep.simxGetObjectHandle(clientID, 'Robot', opmode_blocking)[1]

        # start the simulation:
        vrep.simxStartSimulation(clientID,vrep.simx_opmode_blocking)
        vrep.simxSynchronousTrigger(clientID)

        # Now step a few times:
        for t in range(1,500):
            vrep.simxSynchronousTrigger(clientID)
            
            _, lrf_bin = vrep.simxGetStringSignal(clientID, 'LiDAR', opmode_blocking)
            lrf = np.array(vrep.simxUnpackFloats(lrf_bin), dtype=float)

            # control input 
            v = 1
            theta = 0.1
            # apply control input to the actuators
            R = L/theta
            deltaLeft = np.atan2(L,R+w/2)
            deltaRight = np.atan2(L,R-w/2)
            vrep.simxSetJointTargetPosition(clientID, joint_handle[0], deltaLeft, opmode_blocking)
            vrep.simxSetJointTargetPosition(clientID, joint_handle[1], deltaRight, opmode_blocking)

            vrep.simxSetJointTargetVelocity(clientID, joint_handle[2], v, opmode_blocking)
            vrep.simxSetJointTargetVelocity(clientID, joint_handle[3], v, opmode_blocking)

        # stop the simulation:
        vrep.simxStopSimulation(clientID,vrep.simx_opmode_blocking)

        # Now close the connection to V-REP:
        vrep.simxFinish(clientID)
    else:
        print ('Failed connecting to remote API server')
    print ('Program ended')