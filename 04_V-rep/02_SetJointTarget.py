from __future__ import print_function
import time
from api import vrep
from math import pi

try:
    vrep.simxFinish(-1) # just in case, close all opened connections
except:
    pass

clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to V-REP
if clientID!=-1:
    print ('Connected to remote API server')

    #Get joint handle
    #(
            #client ID,
            #'joint name',
            #operation mode
    #)
    e,handle=vrep.simxGetObjectHandle(clientID,'Revolute_joint',vrep.simx_opmode_blocking)

    #Start simulation(
        #client ID,
        #operation mode
    #)
    vrep.simxStartSimulation(clientID,vrep.simx_opmode_blocking)

    #Set joint target position
    #(
           #client ID,
           #joint handle,
           #target position,
           #operation mode
    #)
    vrep.simxSetJointTargetPosition(clientID,handle,pi/4,vrep.simx_opmode_blocking)
    time.sleep(3)
    
    #Set joint target velocity
    #(
           #client ID,
           #joint handle,
           #target velocity,
           #operation mode
    #)
    vrep.simxSetJointTargetVelocity(clientID,handle,pi/4,vrep.simx_opmode_blocking)
    time.sleep(3)

    #Stop simulation(
        #client ID,
        #operation mode
    #)
    vrep.simxStopSimulation(clientID,vrep.simx_opmode_blocking)

    # Now close the connection to V-REP:
    vrep.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')
