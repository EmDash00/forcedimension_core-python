Installation
============

Install the Package via PyPI
----------------------------

A package is available on PyPI. The most recent version will always support
every supported Python version at the time of release (currently ≥3.8).

.. code-block:: bash

   python3 -m pip install forcedimension_core

Install the Force Dimension SDK
-------------------------------

Go to https://www.forcedimension.com/software and install the latest version of the SDK.
The library will always check that the SDK version installed is greater than the version
that it targets (i.e. v3.16.0 is assumed to be compatible with v3.15.0).

This release of the Force Dimension Python Bindings targets v3.14.0. The library will search
in the following locations to find the Force Dimension SDK dynamic link libraries.

On Mac/Linux:

-  ``/usr/local/lib``
-  ``/usr/lib``

On Windows:

-  ``C:\Program Files\Force Dimension\sdk-X.X.X\lib``


Windows System-Wide Install
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run the executable under the link provided and use the default installation location.

Mac/Linux System-Wide Install
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add the following to the Makefile included in the library's root folder, replacing ``X.X.X``
with your version. Then run ``make install``. If you installed a previous version, this will change the
default installation version to the one you are installing.

.. code-block:: make

  install:
    cp include/* /usr/local/include
    cp lib/release/lin-*-gcc/* /usr/local/lib
    chmod 755 /usr/local/lib/libdhd.so.X.X.X
    chmod 755 /usr/local/lib/libdrd.so.X.X.X
    chmod 755 /usr/local/lib/libdhd.a
    chmod 755 /usr/local/lib/libdrd.a
    ln -s /usr/local/lib/libdhd.so /usr/local/lib/libdhd.so.X.X.X
    ln -s /usr/local/lib/libdrd.so /usr/local/lib/libdrd.so.X.X.X

  uninstall:
    rm /usr/local/include/dhdc.h
    rm /usr/local/include/drdc.h
    rm /usr/local/lib/libdhd.a
    rm /usr/local/lib/libdhd.so.X.X.X
    rm /usr/local/lib/libdhd.so
    rm /usr/local/lib/libdrd.a
    rm /usr/local/lib/libdrd.so.X.X.X
    rm /usr/local/lib/libdrd.so


Non-System-Wide Installs
^^^^^^^^^^^^^^^^^^^^^^^^

If you don't wish to make a system-wide installation, simply set the
``FORCEDIM_SDK`` environment variable to the root folder of the Force Dimension
SDK installation (the ``lib`` folder should be one level under the root installation folder).
This may be desirable if you do not have administrator-level priveleges for your system.

.. note::
  The ``FORCEDIM_SDK`` environment variable takes over default search directories
  (i.e. if it is set, the library will always load from there instead of the default
  search directories). This can be helpful if you have multiple versions of
  the Force Dimension SDK.


Additional Setup
----------------

.. note::
   The following steps require administrator level priveleges.

Windows
^^^^^^^

You may need to install additional drivers for your device if you have not already done so.
To do so, open Device Manager.

In Device Manager, find your haptics device and right-click on it and open ``Properities``.
Then select from the menu ``Update driver>Browse my computer for driver software`` and specify
the drivers listed under ``C:\Program Files\ForceDimension\sdk-X.X.X\drivers\usb``. Try restarting if drivers
are not detected or changes do not take place.

Your device should now be listed under a group called ``USB Haptic Devices``.

Linux
^^^^^

Add a udev rule under ``/etc/udev/rules.d/`` for your device. Make a file called ``40-haptic-device-udev.rules``,
using the name of your device (without spaces) in place of "haptic-device". Then paste in the following template.

::

  ATTR{idVendor}=="", ATTR{idProduct}=="", MODE="0666", SYMLINK+="haptic_device_%k", GROUP="plugdev"
  SUBSYSTEM=="usb", ACTION=="add", ENV{DEVTYPE}=="usb_device", ATTR{idVendor}=="", ATTR{idProduct}=="", MODE="0664", GROUP="plugdev"

Fill in the ``ATTR{idVendor}`` and ``ATTR{idProduct}`` fields with the vendor and product IDs for your device.
Like the file name for ``SYMLINK+="haptic_device_%k`` use the name of your device (without spaces)
in place of "haptic_device".

You can find the vendor and product IDs using ``lsusb``, which lists them in the format
``idVendor:idProduct``. If you are unsure of which device is your haptic device, simply
unplug your device's USB A to B cable and replug it, noting the device that appeared/disappeared
from the list.
