all = [
    'PVGeoReaderBase',
]

from . import _helpers

# Outside Imports:
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase
import numpy as np


# Base Reader
class vtkPVGeoReaderBase(VTKPythonAlgorithmBase):
    def __init__(self, nOutputPorts=1, outputType='vtkTable'):
        VTKPythonAlgorithmBase.__init__(self,
            nInputPorts=0,
            nOutputPorts=nOutputPorts, outputType=outputType)
        self.__dt = 1.0
        self.__timesteps = None
        self.__fileNames = []


    def _get_update_time(self, outInfo):
        # USAGE: i = self._get_update_time(outInfo.GetInformationObject(0))
        executive = self.GetExecutive()
        timesteps = self.__timesteps
        if timesteps is None or len(timesteps) == 0:
            return 0
        elif outInfo.Has(executive.UPDATE_TIME_STEP()) and len(timesteps) > 0:
            utime = outInfo.Get(executive.UPDATE_TIME_STEP())
            return np.argmin(np.abs(timesteps - utime))
        else:
            # if we cant match the time, give first
            assert(len(timesteps) > 0)
            return 0


    def RequestInformation(self, request, inInfo, outInfo):
        self.__timesteps = _helpers.updateTimesteps(self, outInfo, self.__fileNames, self.__dt)
        return 1


    #### Seters and Geters ####
    def SetTimeSteps(self,timesteps):
        """Only use this internally"""
        self.__timesteps = timesteps
        self.Modified()

    def GetTimeSteps(self):
        return self.__timesteps

    def SetTimeDelta(self,dt):
        if dt != self.__dt:
            self.__dt = dt
            self.Modified()

    def ClearFileNames(self):
        self.__fileNames = []

    def AddFileName(self, fname):
        if isinstance(fname, list):
            for f in fname:
                self.AddFileName(f)
        elif fname not in self.__fileNames:
            self.__fileNames.append(fname)
        self.Modified()

    def GetFileNames(self, idx=None):
        if idx is None:
            return self.__fileNames
        return self.__fileNames[idx]
