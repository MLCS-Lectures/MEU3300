<<<<<<< HEAD
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

    #Get object handle
    #(
            #client ID,
            #'object name',
            #operation mode
    #)
    e,handle=vrep.simxGetObjectHandle(clientID,'Cuboid',vrep.simx_opmode_blocking)
    time.sleep(3)

    #Set object position
    #(
           #client ID,
           #object handle,
           #relative to object handle (-1 if absolute),
           #position,
           #operation mode
    #)
    vrep.simxSetObjectPosition(clientID,handle,-1,[0.0,0.0,1.0],vrep.simx_opmode_blocking)
    time.sleep(3)
    
    #Set object orientation
    #(
           #client ID,
           #object handle,
           #relative to object handle (-1 if absolute),
           #orientation,
           #operation mode
    #)
    vrep.simxSetObjectOrientation(clientID,handle,-1,[0.0,0.0,pi/4],vrep.simx_opmode_blocking)

    # Now close the connection to V-REP:
    vrep.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')
=======
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

    #Get object handle
    #(
            #client ID,
            #'object name',
            #operation mode
    #)
    e,handle=vrep.simxGetObjectHandle(clientID,'Cuboid',vrep.simx_opmode_blocking)
    time.sleep(3)

    #Set object position
    #(
           #client ID,
           #object handle,
           #relative to object handle (-1 if absolute),
           #position,
           #operation mode
    #)
    vrep.simxSetObjectPosition(clientID,handle,-1,[0.0,0.0,1.0],vrep.simx_opmode_blocking)
    time.sleep(3)
    
    #Set object orientation
    #(
           #client ID,
           #object handle,
           #relative to object handle (-1 if absolute),
           #orientation,
           #operation mode
    #)
    vrep.simxSetObjectOrientation(clientID,handle,-1,[0.0,0.0,pi/4],vrep.simx_opmode_blocking)

    # Now close the connection to V-REP:
    vrep.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')
>>>>>>> temp
