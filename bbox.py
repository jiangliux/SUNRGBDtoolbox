class Bbox3d:
    def __init__(self, basis, coeffs, centroid, **kwargs):
        self.basis = basis
        self.coeffs = coeffs
        self.centroid = centroid
        self.className = kwargs['className']
        self.sequenceName = kwargs['sequenceName']
        self.orientation = kwargs['orientation']
        self.label = kwargs['label']

    def getConner(self):
        pass
