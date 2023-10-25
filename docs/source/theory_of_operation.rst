Theory of Operation
===================

.. note::
  Prior to v0.1.0, the bindings were included in the ``forcedimension`` Python package; however, as of
  ``forcedimension`` v0.2.0-rc.1, that package only contains higher level wrappers.
  The low level bindings were refactored here as to not have dependencies such as numpy.


Python's ``ctypes`` mechanism allows Python to call C code in dynamically linked library files
(``.dll`` on Windows and ``.so`` on Unix). Other mechanisms to call C/C++ code from Python exist like
Cython for example. ``ctypes`` was chosen primarily for its simplicity.

What the Force Dimension Python Bindings Are and Aren't
-------------------------------------------------------

What they Are
^^^^^^^^^^^^^

The Force Dimension Python Bindings provide the ``forcedimension_core`` Python package. This package directly binds
functions in the Force Dimension SDK's C/C++ API and expose them to Python. The bindings are lightweight, documented
and most of all, typed. Argument typing is enforced by ``ctypes`` using their argtypes mechanism. The bindings also hide
any reference to raw pointers. In combination this allows users to interact with Force Dimension safely with idiomatic
Python without sacrificing performance. The bindings strive for cross-compatability. They are always compatible with
every LTS release of Python (at the time of release). They never depend on outside Python libraries that are not
cross-platform.

What they Aren't
^^^^^^^^^^^^^^^^

The Force Dimension Python Bindings do not aim to improve upon the Force Dimension SDK. It doesn't aim to make
the Force Dimension SDK object oriented. The bindings have no bells and whistles. It aims to have as few
dependencies as possible and is in no case "full feature". They are meant to be used to  do low-level interaction
the C/C++ API from Python with little overhead. This allows the bindings to be used in higher level libraries such as
``forcedimension``.
