import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
import cv2
from utils import *

# read data from mat
SUNRGBDMeta = sio.loadmat('./Metadata/SUNRGBDMeta.mat')['SUNRGBDMeta']
imageId = 31
data = SUNRGBDMeta[0, imageId]

rgbImg = cv2.imread(data['rgbpath'][0])
plt.imshow(rgbImg)
plt.show()

# read data from readFrame