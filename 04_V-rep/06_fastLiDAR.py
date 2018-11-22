from __future__ import print_function, absolute_import, division
import numpy as np
from api import vrep
from matplotlib import pyplot as plt  # matplotlib library required. you can install via pip.


# function for read and unpack string signals
def readLiDAR(clientID, signalName, opmode):
    e, lrf_bin = vrep.simxGetStringSignal(clientID, signalName, opmode)
    if e != -1:
        return 0, np.array(vrep.simxUnpackFloats(lrf_bin), dtype=float)
    else:
        return -1, None


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

        # start the simulation:
        vrep.simxStartSimulation(clientID,vrep.simx_opmode_blocking)
        vrep.simxSynchronousTrigger(clientID) # skip first timestep. LiDAR returns zero-size array at first timestep

        # get LiDAR measurement
        vrep.simxSynchronousTrigger(clientID)
        e, lrf = readLiDAR(clientID, 'measurement', opmode_blocking)

        # plot measurement
        theta = np.linspace(0, 2*np.pi, len(lrf))
        polarplot = plt.polar(theta, lrf)
        plt.show(polarplot)

        # stop the simulation:
        vrep.simxStopSimulation(clientID,vrep.simx_opmode_blocking)

        # Now close the connection to V-REP:
        vrep.simxFinish(clientID)
    else:
        print ('Failed connecting to remote API server')
    print ('Program ended')
