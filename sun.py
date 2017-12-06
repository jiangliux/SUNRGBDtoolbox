import json
import os
import time

import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
from PIL import Image


class SUN:
    def __init__(self, meta_file='./Metadata/SUNRGBDMeta.mat'):
        if not meta_file == None:
            print('loading annotations into memory...')
            tic = time.time()
            self.dataSet = sio.loadmat(meta_file)['SUNRGBDMeta']
            print('Done (t={:0.2f}s)'.format(time.time() - tic))

    def load3dPoints(self, id):
        """
        read points from certain room
        :param id: pos in metadata
        :return: 3d points
        """
        data = self.dataSet[0, id]
        depthVis = Image.open(data['depthpath'][0], 'r')
        depthVisData = np.asarray(depthVis, np.uint16)
        depthInpaint = np.bitwise_or(np.right_shift(depthVisData, 3), np.left_shift(depthVisData, 16 - 3))
        depthInpaint = depthInpaint.astype(np.single) / 1000
        depthInpaint[depthInpaint > 8] = 8
        rgb, points3d, _ = self.load3dPoints_(depthInpaint, data['K'], data['rgbpath'][0])
        points3d = data['Rtilt'].dot(points3d.T).T
        return rgb, points3d, depthInpaint

    def load3dPoints_(self, depth, K, rgbpath):
        cx, cy = K[0, 2], K[1, 2]
        fx, fy = K[0, 0], K[1, 1]
        invalid = depth == 0
        im = np.asarray(Image.open(rgbpath))
        rgb = im.astype(np.double) / np.iinfo(im.dtype).max
        rgb = rgb.reshape(-1, 3)
        x, y = np.meshgrid(np.arange(depth.shape[1]), np.arange(depth.shape[0]))
        xw = (x - cx) * depth / fx
        yw = (y - cy) * depth / fy
        zw = depth
        points3dMatrix = np.stack((xw, zw, -yw), axis=2)
        points3dMatrix[np.stack((invalid, invalid, invalid), axis=2)] = np.nan
        points3d = points3dMatrix.reshape(-1, 3)
        return rgb, points3d, points3dMatrix

    def visPointCloud(self, id):
        data = self.dataSet[0, id]
        rgb, points3d, depth = self.load3dPoints(id)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(points3d[:, 0], points3d[:, 1], points3d[:, 2], c=rgb)
        plt.show()

    def visCube(self, bb3d, color='r', lineWidth=0.5):
        pass


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

    def readFrame(self, framePath, dataRootPath='/data1/', cls=set(), bbmode='bb3d', bfx=False):
        if not os.path.isdir(framePath):
            pass  # TODO: throw exception

        self.sequenceName = self.getSequenceName(framePath, dataRootPath)
        self.sensorType = self.sequenceName.split(os.sep)[1]
        self.K = np.loadtxt(os.path.join(framePath, 'intrisics.txt')).reshape((3, 3))
        self.depthpath = os.path.join(framePath, 'depth_bfx') if bfx else os.path.join(framePath, 'depth')
        self.depthpath += os.listdir(self.depthpath)[0]
        self.rgbpath = os.path.join(framePath, 'image')
        self.rgbpath += os.listdir(self.rgbpath)[0]

        annotation_file = os.path.join(framePath, 'annotation3Dfinal', 'index.json')
        if os.path.isfile(annotation_file):
            with open(annotation_file, 'r') as f:
                annotateImage = json.load(f)
            for annotation in annotateImage['objects']:
                if annotation['name'] in {'wall', 'floor', 'ceiling'} or (len(cls) > 0 and annotation['name'] in cls):
                    continue
                box = annotation['polygon']

    def getSequenceName(self, thisPath, dataRoot='/data1/'):
        return os.path.relpath(thisPath, dataRoot)
