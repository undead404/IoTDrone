# IoT Drone

## MAVLink

MAVLink a.k.a. Micro Air Vehicle Link is a protocol for communicating with drones (small unmanned vehicles). Its nature is a header-only marshaling library.
MAVLink has been originated in 2009. License - LGPL.
Also, MAVLink is a binary protocol.

MAVLink may use TCP, UDP or a serial port. It is at first used to connect GCS (Ground Control Station) to a drone.

If you choose MAVLink, you should generate a **dialect** for communication. A dialect should be arranged as an XML file of some specific format. Also, there are dialect files for well-known types of vehicles(e.g. pixhawk.xml).
From that XML file, MAVLink's Python scripts generate corresponding module. Available programming languages are:
* C
* C#
* Java
* JavaScript
* Lua 
* Python 2.7+

Python2 is literally MAVLink's "native" language and excellent to write a short script.
