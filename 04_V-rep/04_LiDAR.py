from __future__ import print_function, absolute_import, division
import time
import sys
import math
import numpy as np
from api import vrep

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
            vrep.simxGetObjectHandle(clientID, 'motor_left', opmode_blocking)[1],
            vrep.simxGetObjectHandle(clientID, 'motor_right', opmode_blocking)[1]
        ]

        # get target handle
        robot_handle = vrep.simxGetObjectHandle(clientID, 'Robot', opmode_blocking)[1]

        # start the simulation:
        vrep.simxStartSimulation(clientID,vrep.simx_opmode_blocking)
        vrep.simxSynchronousTrigger(clientID)

        # Now step a few times:
        for t in range(1,500):
            vrep.simxSynchronousTrigger(clientID)
            
            _, lrf_bin = vrep.simxGetStringSignal(clientID, 'measuredDataAtThisTime', opmode_blocking)
            print(lrf_bin)
            lrf = np.array(vrep.simxUnpackFloats(lrf_bin), dtype=float)
            print(lrf)


            # control input 
            if np.min(lrf) >0.1:
                u1 = 1
                u2 = 1
            else:
                u1 = 0
                u2 = 0
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
