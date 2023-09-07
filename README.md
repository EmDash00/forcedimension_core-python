# forcedimension_core-python

![license](https://img.shields.io/github/v/release/EmDash00/forcedimension_core-python?display_name=tag)

Currently written and mantained Ember Chow. Looking for the documentation? You can find it here:

https://forcedimension_core-python-documentation.readthedocs.io/en/latest/

## About

### What is the Force Dimension SDK?
The Force Dimension SDK is a set of C/C++ functions and drivers created by
[Force Dimension](https://www.forcedimension.com/company/about) for working with Force Dimension haptic devices as well
as the Novint Falcon and controllers that implement their protocol. It is used by many companies and researchers around
the world.

### Why Python?

When these bindings were originally created, the drivers only had Java bindings; however, a lot of research is conducted
using Python and its various scientific computing libraries (`numpy`, `scipy`, `pandas`, `matplotlib`, etc.). While C/C++
is great for systems code for industrial applications, it is cumbersome for research applications. Java is easier, but simply
doesn't have the ecosystem Python has. The logical solution was to create unofficial bindings in Python for the SDK.

The bindings are lightweight and don't try to introduce overhead unless necessary and closely mimic the C/C++ Force Dimension
SDK.

### How Does it Work?

Python's `ctypes` library allows Python to call C code in dynamically linked library files
(`.dll` on Windows and `.so` on Unix). Other mechanisms to call C/C++ code from Python exist like Cython for example. `ctypes`
was chosen because it was relatively easy to include inline docstrings and typing and did not require external tools.

Version 0.1.0 of the bindings was released in the `forcedimension` Python package; however, as of `forcedimension`
v0.2.0rc1, that package only contains higher level wrappers. The low level bindings were refactored here as to not have
dependencies such as `numpy`.

## Installation

The bindings are available for Windows and Linux. As of Force Dimension SDK v3.16.0, Force Dimension did not
include a dynamically linked library for their Mac OS release, which prevents `ctypes` from being used to bind
the functions on that operating system. Work is underway to ask Force Dimension to provide such a file so that these bindings
will function.

The bindings are available through a PyPI package for Python. The most recent version of the library will always support
all supported Python versions at the time of release.

```
    python3 -m pip install forcedimension_core
```

The bindings do not currently download or install the Force Dimension SDK itself. So additional steps are necessary.

### Install the [ForceDimensionSDK](https://www.forcedimension.com/software/sdk) for your computer.
By default, the bindings will search in the following system-wide install locations for the dynamic link libraries.

* System-wide install locations (Linux):
    - `/usr/local/lib`
    - `/usr/lib`
* System-wide install location (Windows):
    - `C:\Program Files\ForceDimension\sdk-X.X.X\lib`

#### Additional Steps for Linux System-Wide Installation

This requires extra steps since the Makefile for the ForceDimensionSDK does not offer a `make install` target for a system-wide install.

1. Copy all files from `lib/release/lin-*-gcc` to `/usr/local/lib`

2. Copy all files from `include` to `/usr/local/include`

3. MAKE SURE the libraries have `755` level access using `chmod`. If they don't applications cannot link or load them.

4. Make a symbolic link to libdhd and libdrd that drop the version so they end in `.so`, so that the file names are `libdhd.so` and `libdrd.so`

These steps can be automated by adding these targets to the Makefile, replacing X with the version numbers of the SDK.

```makefile
install:
	cp include/* /usr/local/include
	cp lib/release/lin-*-gcc/* /usr/local/lib
	chmod 755 /usr/local/lib/libdhd.so.X.X.X
	chmod 755 /usr/local/lib/libdrd.so.X.X.X
	chmod 755 /usr/local/lib/libdhd.a
	chmod 755 /usr/local/lib/libdrd.a
	ln -s /usr/local/lib/libdhd.so /usr/local/lib/libdhd.so.X.X.X
	ln -s /usr/local/lib/libdrd.so /usr/local/lib/libdrd.so.X.X.X
```

```makefile
uninstall:
	rm /usr/local/include/dhdc.h
	rm /usr/local/include/drdc.h
	rm /usr/local/lib/libdhd.a
	rm /usr/local/lib/libdhd.so.X.X.X
	rm /usr/local/lib/libdhd.so
	rm /usr/local/lib/libdrd.a
	rm /usr/local/lib/libdrd.so.X.X.X
	rm /usr/local/lib/libdrd.so
```

### Non-system-wide Installs

If you do not wish to make a system-wide installation set the FORCEDIM_SDK environment variable to the root folder of the Force
Dimension SDK installation (the `lib` folder should be one level under the root installation folder)

#### Additional Setup

##### Windows

Device Manager is a Windows tool that can be used to see connected devices, their statuses, driver information, and driver installation.

The easiest way to bring it up is to use the windows search bar on Windows 10/11 and search “Device Manager”. Regardless of the method used, you will need administrator level privileges to launch the Device Manager.

Find your haptics device and right-click on it and open `Properities`. Do `Update driver>Browse my computer for driver software` and specify the drivers listed under the `drivers\usb` in the root install directory of the SDK (default is `C:\Program Files\ForceDimension\sdk-X.X.X`). Try restarting if drivers are not detected or changes do not take place.

Your device should now be listed under `USB Haptic Devices`

##### Linux

Add a udev rule under `/etc/udev/rules.d` for your device. Here's an explaination from the [Arch Linux Wiki](https://wiki.archlinux.org/index.php/Udev#Waking_from_suspend_with_USB_device) about what they are and here's a good udev file for the [Novint Falcon](https://github.com/libnifalcon/libnifalcon/blob/master/linux/40-novint-falcon-udev.rules). You can use this format for other devices by changing the name of the file and the idVendor and idProduct

A good way to find the USB bus of the device is by unplugging the device, doing `ls -l /dev/bus/usb/00*`, replugging, the device and then performing it again.

MAKE SURE you unplug the USB and not just the power because the unpowering the device does not unpower the USB communications (which get power through the computer).

Then perform `lsusb` and note the ID of your device, which is in the format `idVendor:idProduct`

## Licensing and Rights

This project is NOT directly associated with Force Dimension. It does NOT involve reverse-engineering or distribution
of proprietary code. Docstrings are lifted from the Force Dimension SDK documentation and revised to fit the Python bindings
with the express permission of Force Dimension.

The Python code itself is licensed under GPLv3 for the benefit of public research.
