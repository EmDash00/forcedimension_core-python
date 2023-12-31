# forcedimension_core-python

![PyPI - Version](https://img.shields.io/pypi/v/forcedimension_core?logo=pypi)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/forcedimension_core?logo=python)  
[![tests](https://github.com/EmDash00/forcedimension_core-python/actions/workflows/tests.yml/badge.svg)](https://github.com/EmDash00/forcedimension_core-python/actions/workflows/tests.yml)
[![Coveralls branch](https://img.shields.io/coverallsCoverage/github/EmDash00/forcedimension_core-python?branch=main&logo=coveralls)](https://coveralls.io/github/EmDash00/forcedimension_core-python)
[![Read the Docs](https://img.shields.io/readthedocs/forcedimension-core-python-docs?logo=Read%20the%20Docs)](https://forcedimension-core-python-docs.readthedocs.io/en/v1.0.0/)  
[![PyPI - License](https://img.shields.io/pypi/l/forcedimension_core)](LICENSE)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)

Want to do more with the Force Dimension SDK with less code? Also check out
the [experimental high level wrappers](https://github.com/EmDash00/forcedimension-python).

## Installation

v1.0.0 of the bindings bind Force Dimension SDK v3.16.0+. They are available through a PyPI package for Python 3.8+.

```
python3 -m pip install forcedimension-core
```

NumPy is an optional dependency which allows the usage of special NumPy style
[containers](https://forcedimension-core-python-docs.readthedocs.io/en/v1.0.0-dev/direct_copy_optimization.html).

```
python3 -m pip install "forcedimension-core[numpy]"
```


You will also need to install the Force Dimension SDK and setup any drivers
or udev rules. If you are unfamiliar with how to do this please refer to the
[detailed installation instructions](https://forcedimension-core-python-docs.readthedocs.io/en/latest/installation.html).

## About

This project aims to create unofficial Python bindings for the Force Dimension SDK's C/C++ API.

```py
import sys
from forcedimension_core import dhd
from forcedimension_core.dhd.os_independent import kbHit, kbGet

b = 5  # damping coefficient in [N][s]/[m]
k = 150  # spring constant in [N]/[m]

# Storage buffers
pos = [0.0, 0.0, 0.0]
v = [0.0, 0.0, 0.0]
f = [0.0, 0.0, 0.0]

# Try to open the first available device
if (ID := dhd.open()) == -1:
  print(f"Error: {dhd.errorGetLastStr()}")
  sys.exit(1)

if (name := dhd.getSystemName()) is not None:
  print(isinstance(name, str))  # prints "True"
  print(name)

# Run until button 0 is pressed (typically the center or only button)
# or q is pressed on the keyboard
try:
  while not (dhd.getButton(index=0) or (kbHit() and kbGet() == 'q')):
    # Try to get the position
    if (dhd.getPosition(out=pos) == -1):
      raise dhd.errno_to_exception(dhd.errorGetLast())(
        op=dhd.getPosition, ID=ID
      )

    # Try to get the velocity
    if (dhd.getLinearVelocity(out=v) == -1):
      raise dhd.errno_to_exception(dhd.errorGetLast())(
        op=dhd.getLinearVelocity, ID=ID
      )

    # Set the dynamics to be a spring-mass damper
    f[0] = -k * pos[0] - b * v[0]
    f[1] = -k * pos[1] - b * v[1]
    f[2] = -k * pos[2] - b * v[2]

    # Try to set the force
    if (dhd.setForce(f) == -1):
      raise dhd.errno_to_exception(dhd.errorGetLast())(
        op=dhd.setForce, ID=ID
      )
except Exception as ex:
    print(str(ex))
finally:
  # On error, close the device and gracefully exit
  dhd.close(ID)
  sys.exit(1)
```

## Licensing and Rights

This project is NOT directly associated with Force Dimension. It does NOT involve reverse-engineering or distribution
of proprietary code. Docstrings are lifted from the Force Dimension SDK documentation and revised to fit the Python bindings
with the express permission of Force Dimension.

The Python code itself is licensed under LGPLv3 for the benefit of public
research.
