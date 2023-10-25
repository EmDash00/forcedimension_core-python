.. ForceDimension Python Bindings documentation master file, created by
   sphinx-quickstart on Tue Jul 19 13:59:28 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the Force Dimension Python Bindings Documentation!
===============================================================

The Force Dimension Python Bindings allow users to interact with the Force Dimension SDK's
C/C++ API in Python.

.. code-block:: python

  import sys
  from forcedimension_core import dhd

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
    while not (
      dhd.getButton(index=0) or
      (dhd.os_independent.kbHit() and dhd.os_independent.kbGet() == 'q')
    ):
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

Copyright
=========
The Force Dimension SDK and documentation is property of Force Dimension, all rights reserved.
This project is NOT directly associated with Force Dimension. It does NOT involve reverse-engineering
or distribution of proprietary code. Docstrings are lifted from the Force Dimension SDK documentation
and revised to fit the Python bindings with the express permission of Force Dimension.

The Python code itself is licensed under GPLv3 for the benefit of public research.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   modules.rst
   installation.rst
   theory_of_operation.rst
   direct_copy_optimization.rst
   forcedimension_core.dhd-doc.rst
   forcedimension_core.drd-doc.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
