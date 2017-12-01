from .getSequenceName import *
import os
import numpy as np
class FrameData:
    def __init__(self, sequenceName='', groundTruth3DBB=None, Rtilt=None, K=None, depthpath='', rgbpath='',
                 anno_extrinsics=None, sensorType='', gtCorner3D=None):
        self.sequenceName = sequenceName
        self.groundTruth3DBB = groundTruth3DBB
        self.Rtilt = Rtilt
        self.K = K
        self.depthpath = depthpath
        self.rgbpath = rgbpath
        self.anno_extrinsics = anno_extrinsics
        self.sensorType = sensorType
        self.gtCorner3D = gtCorner3D

    def readFrame(self, framePath, dataRootPath='/data1/', cls=[], bbmode='bb3d', bfx=False):
        if not os.path.isdir(framePath):
            pass # TODO: throw exception

        self.sequenceName = getSequenceName(framePath, dataRootPath)
        self.sensorType = self.sequenceName.split(os.sep)[1]
        self.K = np.loadtxt(os.path.join(framePath, 'intrisics.txt')).reshape((3,3))
        self.depthpath = os.path.join(framePath, 'depth_bfx') if bfx else os.path.join(framePath, 'depth')
        self.depthpath += os.listdir(self.depthpath)[0]
        self.rgbpath = os.path.join(framePath, 'image')
        self.rgbpath += os.listdir(self.rgbpath)[0]
        

