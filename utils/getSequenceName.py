import os

def getSequenceName(thisPath, dataRoot='/data1/'):
    return os.path.relpath(thisPath, dataRoot)