# Python Bindings for ContamX 

**NOTE: This package is not yet fully functional.**

This is the initial implementation of a Python wrapper for `contamx-lib.lib` which is a statically linked library with an API wrapper around ContamX. `contamx-lib` enables control of CONTAM simulations via C-language API. This Python package, `contamxpy`, provides another layer of access, i.e., Python bindings, to `contamx-lib`.  

The demonstration driver, `test_cxffi.py` that is included herein, imports `contamxpy`, obtains a `state`, gets properties of the simulation necessary to run from beginning to end, then steps through all the time steps.  

# Usage

Typically, one would work within a Python virtual environment which can be created and activated using the following commands.  
```
$ python -m venv .venv
$ .venv\Scripts\activate  (on Windows)
```   
Install `contamxpy` from PyPI.  
```
$(.venv) python -m pip install contamxpy
```   
Get help for the test module from the command line.
```
test_cxcffi.py -h

Usage: test_cxcffi.py [options] arg1  
    arg1=PRJ filename

Options:
  -h, --help    show this help message and exit
  -v VERBOSE, --verbose=VERBOSE
                define verbose output level: 0=Min, 1=Medium,
                2=Max
```
Run example case.
```
test_cxcffi.py testOneZoneWthCtm.prj
```
## Example Test Module: *test_cxcffi.py*  
```python
from contamxpy import cxLib 
import os, sys
from optparse import OptionParser

#===================================================================================== main() =====
def main():
    #----- Manage option parser
    parser = OptionParser(usage="%prog [options] arg1\n\targ1=PRJ filename\n")
    parser.set_defaults(verbose=0)
    parser.add_option("-v", "--verbose", action="store", dest="verbose", type="int", default=0,
                        help="define verbose output level: 0=Min, 1=Medium, 2=Maximum.")
    (options, args) = parser.parse_args()

    #----- Process command line options -v
    verbose = options.verbose

    if len(args) != 1:
        parser.error("Need one argument:\n  arg1 = PRJ file.")
        return
    else:
        prj_name  = args[0]

    if ( not os.path.exists(prj_name) ):
        print("ERROR: PRJ file not found.")
        return

    msg_cmd = "Running test_cxcffi.py: arg1 = " + args[0] + " " + str(options)
    print(msg_cmd, "\n")

    if verbose > 1:
        print(f"cxLib attributes =>\n{chr(10).join(map(str, dir(cxLib)))}\n")

    #----- Initialize contamx-lib object w/ wpMode and cbOption.
    #      wpMode = 0 => use wind pressure profiles, WTH and CTM files or associated API calls.
    #      cbOption = True => set callback function to get PRJ INFO from the ContamXState.
    myPrj = cxLib(0, True)
    myPrj.setVerbosity(verbose)
    if verbose > 1:
        print(f"BEFORE setupSimulation()\n\tnCtms={myPrj.nContaminants}\n\tnZones={myPrj.nZones}\n\tnPaths={myPrj.nPaths}\n" )
    
    #----- Query State for Version info
    verStr = myPrj.getVersion()
    if verbose >= 0:
        print(f"getVersion() returned {verStr}.")

    #----- Setup Simulation for PRJ
    myPrj.setupSimulation(prj_name, 1)

    if verbose > 1:
        print(f"AFTER setupSimulation()\n\tnCtms={myPrj.nContaminants}\n\tnZones={myPrj.nZones}\n\tnPaths={myPrj.nPaths}\n" )

    dayStart = myPrj.getSimStartDate()
    dayEnd   = myPrj.getSimEndDate()
    secStart = myPrj.getSimStartTime()
    secEnd   = myPrj.getSimEndTime()
    tStep    = myPrj.getSimTimeStep()

    simBegin = (dayStart - 1) * 86400 + secStart
    simEnd = (dayEnd - 1) * 86400 + secEnd
 
    #----- Calculate the simulation duration in seconds and total time steps
    if (simBegin < simEnd):
        simDuration = simEnd - simBegin
    else:
        simDuration = 365 * 86400 - simEnd + simBegin
    numTimeSteps = int(simDuration / tStep)
 
    #----- Get the current date/time after initial steady state simulation
    currentDate = myPrj.getCurrentDayOfYear()
    currentTime = myPrj.getCurrentTimeInSec()
    if verbose > 0:
        print(f"Sim days = {dayStart}:{dayEnd}")
        print(f"Sim times = {secStart}:{secEnd}")
        print(f"Sim time step = {tStep}")
        print(f"Number of steps = {numTimeSteps}")

    #----- Run Simulation
    for i in range(numTimeSteps):
        currentDate = myPrj.getCurrentDayOfYear()
        currentTime = myPrj.getCurrentTimeInSec()
        if verbose > 1:
            print(f"{i}\t{currentDate},{currentTime}")
        myPrj.doSimStep(1)

    myPrj.endSimulation()

# --- End main() ---#

if __name__ == "__main__":
    main()
```

# Developer Notes

These bindings were developed using the **C Foreign Function Interface (CFFI)**. CFFI utilizes C header files that define the `contamx-lib` API. `contamx-lib.lib` is a build of ContamX that is statically linked build of `contamx-lib`. A dynamic Python module (.pyd) is built that incorporates the static build.  

**NIST Developer NOTE:** The static build of `contamx-lib.lib` must include the following dependencies: `WSock32.lib`, `WS2_32.lib`, and `user32.lib`.  

## Steps to Develop Python Bindings

### 1. Create directory for *contamxpy*  
- Either clone the repo (NIST developers only) OR
- Download the source distribution from https://pypi.org/project/contamxpy/  
#### Source files:  

```
contamxpy\  
|
| setup.py
| setup.cfg
| MANIFEST.in 
| LICENSE.txt
| README.md
| contamxpy_build.py
| contamxpy.py
| contamx-lib.lib
|
├── include\
|   └── common-api.h
|       commonState.h
|       contam-x-cosim.h
|       contam-x-state.h
|       element-api.h
|       flags.h
|       library-api.h
|       project-api.h
|       string-len-max.h
|       types.h
|
└── demo_files\
    └── test_cxcffi.py
        testOneZoneWthCtm.prj/.wth/.ctm
        valThreeZonesWth.prj/.wth/.ctm
```
### 2. Create virtual environment
   `python -m venv .venv`  
   
### 3. Activate virtual environment
   + Windows => `.venv\Scripts\activate.bat`
   
### 4. Install *cffi* and *wheel* packages  
   `$ python -m pip install cffi, wheel`

### 5. Generate *contamxpy* 

Run the build module.
```
contamxpy_build.py
```   
This should generate *_contamxpy.c*, etc.
```
contamxpy\  
|
├── Release\
|   └── *.exp/.lib/.obj
|
└── _contamxpy.c
    _contamxpy.cp310-win_amd64.pyd
```

Most importantly it will generate a .pyd file, e.g., 
`_contamxpy-0.0.3-abi3-cp310-win_amd64.pyd`. This is a dynamic Python module to be imported into a driver program. It provides a wrapper to `contamx-lib.lib`. 

### 6. Install the development version locally
```
$(.venv) pip install .
```
### 7. Generate Files for Distribution
Built distribution, i.e., wheel file:
```
$(.venv) python -m setup bdist_wheel
```
Source distribution, i.e., compressed archive (.gz, .zip):
```
$(.venv) python -m setup sdist
$(.venv) python -m setup sdist --format=zip
```

## Development Files  

### cxcffi_build.py

The file shown below is a partial implementation of the 
API associated with `contamx-lib`.  

```python
from __future__ import annotations

# Using the "out-of-line", "API mode"
from cffi import FFI


CDEF = '''\
    // see types.h
    typedef int32_t IX;
    typedef float R4;
    typedef double R8;
    typedef uint16_t U2;
    
    typedef struct zone_cosim_dsc
    {
        int32_t nr;
        uint16_t flags;
        float Vol;
        char level_name[16]; // #define NAMELEN 16
        int32_t level_nr;
        char name[32];       // #define NMLN 32
    } ZONE_COSIM_DSC;

    typedef struct path_cosim_dsc 
    {
        IX nr;
        U2 flags;
        IX from_zone;
        IX to_zone;
        IX ahs_nr;
        R4 X;
        R4 Y;
        R4 Z;
        IX envIndex;
    } PATH_COSIM_DSC;

    // Callback function - extern => to be python function defined in contamxpy.py.
    extern "Python" void prjDataReadyFcnP(void *, void *);
    // {prjDataReadyFcnP} will set to function defined in {cxLib} class of {contamxpy}.
    void cxiRegisterCallback_PrjDataReady( void* contamXState, void* pUserData, void ( *prjDataReadyFcnP )( void*, void* ) );

    void* cxiGetContamState();
    void cxiSetWindPressureMode(void* contamXState, IX useWP);
    void cxiSetupSimulation(void* contamXState, char* projectPath, IX useCosim);
    IX cxiGetVersion(void* contamXState, char* strVersion);

    IX cxiGetSimulationStartDate(void* contamXState);
    IX cxiGetSimulationStartTime(void* contamXState);
    IX cxiGetSimulationEndDate(void* contamXState);
    IX cxiGetSimulationEndTime(void* contamXState);
    IX cxiGetSimulationTimeStep(void* contamXState);
    IX cxiGetCurrentDate(void* contamXState);
    IX cxiGetCurrentTime(void* contamXState);
    void cxiDoCoSimStep(void* contamXState, IX stepForward);
    void cxiEndSimulation(void* contamXState);

    // These functions will be utilized within the callback function, prjDataReadyFcnP(),
    //   to populate class variables for access by the calling/driver
    //   program which imports {contamxpy}
    IX cxiGetNumCtms(void* contamXState);
    IX cxiGetCtmName(void* contamXState, IX ctmNumber, char* strName);
    IX cxiGetNumZones(void* contamXState);
    IX cxiGetZoneInfo(void* contamXState, IX zoneNumber, ZONE_COSIM_DSC* pZoneInfo);
    IX cxiGetNumPaths(void* contamXState);
    IX cxiGetPathInfo(void* contamXState, IX pathNumber, PATH_COSIM_DSC* pPath);

    // Results
    IX cxiGetZoneMF(void* contamXState, IX zoneNumber, IX ctmNumber, R8* pMassFraction);
'''

SRC = '''\
    #include "include//contam-x-cosim.h"
'''

ffibuilder = FFI()
ffibuilder.cdef(CDEF)
ffibuilder.set_source(
    "_contamxpy", SRC,
    include_dirs=['.','include'],  # C header files for contam-x-lib
    libraries=['contamx-lib'],     # Library to link with (.lib, .dll)
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
```
### contamxpy
`contamxpy` implements the `cxLib` class that provides the wrapper to `contamx-lib`. This module is imported for use by driver programs as demonstrated in *test_cxcffi.py* above.
```python
from __future__ import annotations

import _contamxpy

_lib = _contamxpy.lib
_ffi = _contamxpy.ffi

#print(f"_contamxpy => \n\t{dir(_contamxpy)}")

'''
    cxiGetContamState() is defined in contam-x-cosim.c
'''
def getState():
    return _lib.cxiGetContamState()

def setWindPressureMode(state, mode):
    _lib.cxiSetWindPressureMode(state, mode)

def getVersion(state):
    bufStr = _ffi.new("char[]", 64)
    _lib.cxiGetVersion(state, bufStr)
    return _ffi.string(bufStr).decode('utf-8')

def setupSimulation(state, prjPath, useCosim):
    _lib.cxiSetupSimulation(state, prjPath.encode('ascii'), useCosim)

def getSimTimeStep(state):
    timeStep = _lib.cxiGetSimulationTimeStep(state)
    return timeStep

def getSimStartDate(state):
    dayOfYear = _lib.cxiGetSimulationStartDate(state)
    return dayOfYear

def getSimEndDate(state):
    dayOfYear = _lib.cxiGetSimulationEndDate(state)
    return dayOfYear

def getSimStartTime(state):
    timeOfDaySeconds = _lib.cxiGetSimulationStartTime(state)
    return timeOfDaySeconds

def getSimEndTime(state):
    timeOfDaySeconds = _lib.cxiGetSimulationEndTime(state)
    return timeOfDaySeconds

def getCurrentDayOfYear(state):
    return _lib.cxiGetCurrentDate(state)

def getCurrentTimeInSec(state):
    return _lib.cxiGetCurrentTime(state)

def doSimStep(state, stepForward):
    _lib.cxiDoCoSimStep(state, stepForward)

def endSimulation(state):
    _lib.cxiEndSimulation(state)
```

### setup.py  

```python
from __future__ import annotations

import platform
import sys

from setuptools import setup

if platform.python_implementation() == 'CPython':
    try:
        import wheel.bdist_wheel
    except ImportError:
        cmdclass = {}
    else:
        class bdist_wheel(wheel.bdist_wheel.bdist_wheel):
            def finalize_options(self) -> None:
                self.py_limited_api = f'cp3{sys.version_info[1]}'
                super().finalize_options()

        cmdclass = {'bdist_wheel': bdist_wheel}
else:
    cmdclass = {}

setup(
    cffi_modules=['contamxpy_build.py:ffibuilder'], cmdclass=cmdclass
    )
```

### setup.cfg

```ini
[metadata]
name = contamxpy
version = 0.0.3
description = Python wrapper for the CONTAM Simulation Engine, ContamX
long_description = file: README.md
long_description_content_type = text/markdown
author = W. Stuart Dols, Brian Polidoro, NIST
author_email = william.dols@nist.gov
license = Public Domain
license_files = LICENSE.txt
classifiers =
    License :: Public Domain 
    License :: OSI Approved :: BSD License
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3 :: Only
    Programming Language :: Python :: Implementation :: CPython
    Programming Language :: Python :: Implementation :: PyPy
    Topic :: Scientific/Engineering
project_urls=
    Web Page= https://www.nist.gov/el/energy-and-environment-division-73200/nist-multizone-modeling/
    Source  = https://pypi.org/project/contamxpy/
[options]
py_modules = contamxpy
python_requires = >=3.7
install_requires =
    cffi>=1
setup_requires =
    cffi>=1
```

### MANIFEST.in
The manifest file is used to add files to the source builds.  

```
include include\*.h
include contamx-lib.*
include demo_files\*.*
```

# REFERENCES
1. https://www.youtube.com/watch?v=X5irxO5VCHw
2. https://github.com/asottile/ukkonen
3. https://cffi.readthedocs.io/en/latest/index.html
4. https://docs.python.org/3.10/distutils/index.html
5. https://setuptools.pypa.io/en/latest/setuptools.html
6. https://packaging.python.org/en/latest/tutorials/packaging-projects/

# TODO  
- Implement full API.  
- Test on Linux  
