from sun import SUN
from bbox import Bbox3d


if __name__ == '__main__':
    sunrgbd = SUN()
    # sunrgbd.visPointCloud(31)
    box3d = sunrgbd.dataSet[:, 31]['groundtruth3DBB'][0]
    bb = Bbox3d(box3d['basis'][:, 0][0], box3d['coeffs'][:, 0][0], box3d['centroid'][:, 0][0])
    print(bb.getCorner())
