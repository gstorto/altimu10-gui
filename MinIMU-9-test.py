# MinIMU9ArduinoAHRS
# Pololu MinIMU-9 + Arduino AHRS (Attitude and Heading Reference System)

# Copyright (c) 2011 Pololu Corporation.
# http://www.pololu.com/

# MinIMU9ArduinoAHRS is based on sf9domahrs by Doug Weibel and Jose Julio:
# http://code.google.com/p/sf9domahrs/

# sf9domahrs is based on ArduIMU v1.5 by Jordi Munoz and William Premerlani, Jose
# Julio and Doug Weibel:
# http://code.google.com/p/ardu-imu/

# MinIMU9ArduinoAHRS is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your option)
# any later version.

# MinIMU9ArduinoAHRS is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for
# more details.

# You should have received a copy of the GNU Lesser General Public License along
# with MinIMU9ArduinoAHRS. If not, see <http://www.gnu.org/licenses/>.

################################################################################

# This is a test/3D visualization program for the Pololu MinIMU-9 + Arduino
# AHRS, based on "Test for Razor 9DOF IMU" by Jose Julio, copyright 2009.

# This script needs VPython, pyserial and pywin modules

# First Install Python 2.6.4 (Python 2.7 also works)
# Install pywin from http://sourceforge.net/projects/pywin32/
# Install pyserial from http://sourceforge.net/projects/pyserial/files/
# Install VPython from http://vpython.org/contents/download_windows.html

from visual import *
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", dest="output", help="dump received data from RPi")
    args = parser.parse_args()
    return args

grad2rad = 3.141592/180.0

# Main scene
scene=display(title="Pololu AltiMU-10")
scene.range=(1.2,1.2,1.2)
#scene.forward = (0,-1,-0.25)
scene.forward = (1,0,-0.25)
scene.up=(0,0,1)
scene.width=500
scene.y=200

# Main scene objects
scene.select()
# Reference axis (x,y,z)
arrow(color=color.green,axis=(1,0,0), shaftwidth=0.02, fixedwidth=1)
arrow(color=color.green,axis=(0,-1,0), shaftwidth=0.02 , fixedwidth=1)
arrow(color=color.green,axis=(0,0,-1), shaftwidth=0.02, fixedwidth=1)
# labels
label(pos=(0,0,0.85),text="Rocket Model",box=0,opacity=0)
altitude_l = label(pos=(0,0.9,0),text="0m",box=0,opacity=0)
temperature_l = label(pos=(0,0.91,-0.1),text="0.0c",box=0,opacity=0)
label(pos=(1,0,0),text="X",box=0,opacity=0)
label(pos=(0,-1,0),text="Y",box=0,opacity=0)
label(pos=(0,0,-1),text="Z",box=0,opacity=0)
# IMU object
platform = box(length=1, height=0.05, width=1, color=color.blue)
p_line = box(length=1,height=0.08,width=0.1,color=color.yellow)
plat_arrow = arrow(color=color.green,axis=(1,0,0), shaftwidth=0.06, fixedwidth=1)

roll=0
pitch=0
yaw=0

args = parse_args()
altitude_ref = None
with open(args.output, 'w') as flog:
    while True:
        line = sys.stdin.readline()
        words = filter(None, line.split(' ')) 
        if len(words) > 11:
            try:
                roll = float(words[1])*grad2rad
                pitch = float(words[2])*grad2rad
                yaw = float(words[3])*grad2rad
                altitude = float(words[10])
                if (altitude_ref == None):
                    altitude_ref = altitude
                temperature = float(words[11])
            except:
                continue
            flog.write(line)

            # Updated 3D-model
            axis=(cos(pitch)*cos(yaw),-cos(pitch)*sin(yaw),-sin(pitch)) 
            up=(sin(roll)*sin(yaw)+cos(roll)*sin(pitch)*cos(yaw),
                sin(roll)*cos(yaw)-cos(roll)*sin(pitch)*sin(yaw),
                cos(roll)*cos(pitch))
            platform.axis=axis
            platform.up=up
            platform.length=1.0
            platform.width=0.65
            plat_arrow.axis=axis
            plat_arrow.up=up
            plat_arrow.length=0.8
            p_line.axis=axis
            p_line.up=up
            # Updated Altitude/Temp
            altitude_l.text = "{0:.0f}m".format(altitude-altitude_ref)
            temperature_l.text = "{0:.1f}c".format(temperature)
