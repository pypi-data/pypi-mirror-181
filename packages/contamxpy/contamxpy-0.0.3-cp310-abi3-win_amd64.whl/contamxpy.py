from __future__ import annotations

import _contamxpy

_lib = _contamxpy.lib
_ffi = _contamxpy.ffi

MAX_LEN_VER_STR = 64
NAMELEN = 16          # contaminants, elements, schedules, levels, controls
NMLN2 = 32            # zones

#=========================================================== class Zone  =====#
class Zone:
    def __init__(self, nr, name, f, v, lnr, lname) -> None:
        self.zoneNr = nr
        self.zoneName = name
        self.levNr = lnr
        self.levName = lname
        self.flags = f
        self.volume = v
    
    def __repr__(self):
        return("{}({!r},{!r},{!r},{!r},{!r},{!r})".format( \
            self.__class__.__name__, self.zoneNr, self.zoneName, self.flags, \
            self.volume, self.levNr, self.levName) \
              )

#=========================================================== class Path  =====#
class Path:
    def __init__(self, n, f, zFrom, zTo, ahsNr, x, y, z, envIdx) -> None:
        self.pathNr = n
        self.flags = f
        self.from_zone = zFrom
        self.to_zone = zTo
        self.ahs_nr = ahsNr
        self.X = x
        self.Y = y
        self.Z = z
        self.envIndex = envIdx
    
    def __repr__(self):
        return("{}({!r},{!r},{!r},{!r},{!r},{!r},{!r},{!r},{!r})".format( \
            self.__class__.__name__, self.pathNr, self.flags, \
            self.from_zone, self.to_zone, self.ahs_nr, self.X, self.Y, self.Z, self.envIndex) \
              )

#=========================================================== class cxLib =====#
class cxLib:
    @staticmethod 
    def __convertString(cdataStr):
        return _ffi.string(cdataStr).decode('utf-8')
    
    def __init__(self, wpMode, cbOption):
        #----- Instance Data -----#
        self._self_handle = _ffi.new_handle(self)
        self.state = _lib.cxiGetContamState()
        self.verbose = 0
        #----- PRJ Data -----#
        self.wpMode = wpMode
        self.nContaminants = -1
        self.contaminants = []
        self.nZones = -1
        self.zones = []
        self.nPaths = -1
        self.paths = []

        if wpMode < 0 or wpMode > 1:
            wpMode = 0
        _lib.cxiSetWindPressureMode(self.state, wpMode)
        ### DEBUG
        ###print(f"cxLib __init__() =>\n\tstate=[{self.state}]\n\tself_handle=[{self._self_handle}]\n\tself=[{self}]\n")
        ###print(f"\tnContaminants={self.nContaminants}\n\tnZones={self.nZones}\n\tnPaths={self.nPaths}\n")

        if(cbOption==True):
            # {self._self_handle} is passed through to provide the callback with access 
            #   to the instance of the {cxLib} object.
            _lib.cxiRegisterCallback_PrjDataReady(self.state, self._self_handle, _lib.prjDataReadyFcnP)

    def setVerbosity(self, level):
        self.verbose = max(level,0)

    #---------- contamx-lib: simulation initialization
    def getState(self):
        return _lib.cxiGetContamState()

    def setWindPressureMode(state, mode):
        _lib.cxiSetWindPressureMode(state, mode)

    def getVersion(self):
        bufStr = _ffi.new("char[]", MAX_LEN_VER_STR)
        _lib.cxiGetVersion(self.state, bufStr)
        return cxLib.__convertString(bufStr)

    def setupSimulation(self, prjPath, useCosim):
        _lib.cxiSetupSimulation(self.state, prjPath.encode('ascii'), useCosim)

    #---------- contamx-lib: Simulation properties ----------
    def getSimTimeStep(self):
        timeStep = _lib.cxiGetSimulationTimeStep(self.state)
        return timeStep

    def getSimStartDate(self):
        dayOfYear = _lib.cxiGetSimulationStartDate(self.state)
        return dayOfYear

    def getSimEndDate(self):
        dayOfYear = _lib.cxiGetSimulationEndDate(self.state)
        return dayOfYear

    def getSimStartTime(self):
        timeOfDaySeconds = _lib.cxiGetSimulationStartTime(self.state)
        return timeOfDaySeconds

    def getSimEndTime(self):
        timeOfDaySeconds = _lib.cxiGetSimulationEndTime(self.state)
        return timeOfDaySeconds

    #---------- contamx-lib: Simulation time ----------
    def getCurrentDayOfYear(self):
        return _lib.cxiGetCurrentDate(self.state)

    def getCurrentTimeInSec(self):
        return _lib.cxiGetCurrentTime(self.state)

    #----------- contamx-lib: Simulation control ----------
    def doSimStep(self, stepForward):
        _lib.cxiDoCoSimStep(self.state, stepForward)

    def endSimulation(self):
        _lib.cxiEndSimulation(self.state)

    #----------- Called by prjDataReadyFcnP() ----------
    # These functions are used to populate the list of
    #   items which are members of cxLib instances.
    #
    def getCtmName(self, i):
        nameStr = _ffi.new("char[]", NAMELEN)
        if( i >= 0 and i < self.nContaminants ):
            _lib.cxiGetCtmName(self.state, i, nameStr)
        return cxLib.__convertString(nameStr)

    def getZoneInfo(self, i):
        pz = _ffi.new("ZONE_COSIM_DSC *")
        zoneNameStr = _ffi.new("char[]", NAMELEN)
        levNameStr = _ffi.new("char[]", NAMELEN)

        if( i > 0 and i <= self.nZones ):
            _lib.cxiGetZoneInfo(self.state, i, pz)
            zoneNameStr = cxLib.__convertString(pz.name)
            levNameStr = cxLib.__convertString(pz.level_name)
            zone = Zone(pz.nr, zoneNameStr, pz.flags, pz.Vol, pz.level_nr, levNameStr)
        return zone

    def getPathInfo(self, i):
        pp = _ffi.new("PATH_COSIM_DSC *")

        if( i > 0 and i <= self.nPaths ):
            _lib.cxiGetPathInfo(self.state, i, pp)
            path = Path(pp.nr, pp.flags, pp.from_zone, pp.to_zone, pp.ahs_nr, pp.X, pp.Y, pp.Z, pp.envIndex)
        return path

#===================================================== Callback function =====#
#
@_ffi.def_extern()
def prjDataReadyFcnP(state, handle):
    #----- Get instance of cxLib class from pass-through data handle
    #      created in cxLib.__init__() via new_handle() FFI function.
    cxlib = _ffi.from_handle(handle)
    if cxlib.verbose > 0:
        print(f"prjDataReadFcnP(\n\tstate=[{state}]\n\tpData=[{handle}]\n\tuser_data=[{cxlib}]\n)\n")

    #----- Get data from the state
    #
    cxlib.nContaminants = _lib.cxiGetNumCtms(state)
    cxlib.nZones = _lib.cxiGetNumZones(state)
    cxlib.nPaths = _lib.cxiGetNumPaths(state)
    ### DEBUG ###
    if cxlib.verbose > 0:
        print(f"\tnContaminants={cxlib.nContaminants}\n\tnZones={cxlib.nZones}\n\tnPaths={cxlib.nPaths}\n")

    #----- Get list of Contaminants from contamx-lib
    #
    for i in range(cxlib.nContaminants):
        name = cxlib.getCtmName(i)
        if( len(name) <= 0 ):
            print(f"ERROR: cxiGetCtmName({i})\n")
        else:
            cxlib.contaminants.append(name)
    if(cxlib.verbose > 0):
        print(f"Contaminants = {cxlib.contaminants}\n")

    #----- Get list of Zones from contamx-lib
    #  and populate cxlib zones list with Zone objects.
    #  NOTE: zones indexed from 1->nZones.
    #
    for i in range(cxlib.nZones):
        z = cxlib.getZoneInfo(i+1)
        cxlib.zones.append(z)

    if(cxlib.verbose > 0):
        print(f"Zones = {cxlib.zones}\n")

    #----- Get list of Paths from contamx-lib
    #  and populate cxlib path list with Path objects.
    #  NOTE: paths indexed from 1->nPaths.
    #
    for i in range(cxlib.nPaths):
        p = cxlib.getPathInfo(i+1)
        cxlib.paths.append(p)

    if(cxlib.verbose > 0):
        print(f"Paths = {cxlib.paths}\n")
