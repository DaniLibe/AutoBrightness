#!/usr/bin/python

"""

Python script.
This script will automatically change screen brightness based on data received by the photoresistor connected to the Arduino board. It MUST be run as root!

Author: DaniLibe
Github: https://github.com/DaniLibe
Twitter: https://twitter.com/danilibe98
Mail: danylibedev@gmail.com

If you find a bug contact me on danylibedev@gmail.com
Enjoy! ;)

"""

import serial, os, sys

def main():
    
    if (sys.platform == "linux2"):  # This script works only on Linux platforms
        find_brightness_files()
        get_sensor_data()
    else:
        print "This OS isn't supported by this script! It works only on Linux platforms!"

# This function will find "brightness" and "max_brightness" files
def find_brightness_files():

    global backlight_path
    global file_to_open
    global file_to_open2

    backlight_path = "/sys/class/backlight/"

    # This loop is to avoid common problem linked to acpi_video that sometimes doesn't work
    i = 0
    while (i < len(os.listdir(backlight_path))):
        if (os.listdir(backlight_path)[i].find("acpi_video") == -1):
            file_dir = os.listdir(backlight_path + os.listdir(backlight_path)[i])
            break
        else:
            file_dir = os.listdir(backlight_path + os.listdir(backlight_path)[0])
            i += 1
        
    i = 0
    files_list = ""
    separator = "%break%"
                        
    while (i < len(file_dir)):
        files_list += file_dir[i] + separator
        i += 1

    files = files_list.split(separator)
    i = 0
                          
    while (i < len(files)):
        if (files[i] == "brightness"):
            file_to_open = files[i]

        if (files[i] == "max_brightness"):
            file_to_open2 = files[i]

        i += 1

# This function is the porting of the "constrain(amt, low, high)" function in the Arduino source code (you can find It in "Arduino.h")
def constrain_sensor_values(val, val_min, val_max):

    if (val < val_min):
        return val_min
    elif (val > val_max):
        return val_max
    else:
        return val

# This function will find the serial port to which is connected the Arduino board
def find_serial_port():

    serial_port = None
    i = 0
    
    while (i <= 65535):
        try:
            board_port = serial.Serial("/dev/ttyACM" + str(i))
            board_port.close()
            serial_port = "/dev/ttyACM" + str(i)
            break
        except serial.SerialException:
            i += 1

    if (serial_port == None):
        i = 0

        while (i <= 65535):
            try:
                board_port = serial.Serial("/dev/ttyUSB" + str(i))
                board_port.close()
                serial_port = "/dev/ttyUSB" + str(i)
                break
            except serial.SerialException:
                i += 1

        if (serial_port == None):
            print "Serial port not found!"

    return serial_port

# This function will get screen max brightness
def get_max_brightness():

    max_brightness_file = open(backlight_path + os.listdir(backlight_path)[0] + "/" + file_to_open2, "r")
    max_brightness = max_brightness_file.readline()

    # FOR DEBUG
    #print max_brightness
    
    max_brightness_file.close()

    return max_brightness

# This function will get photoresistor data from the serial port
def get_sensor_data():

    global sensor_data

    if (find_serial_port() != None):
        sensor = serial.Serial(find_serial_port())

        while (True):
            try:
                sensor_data = sensor.readline()
                if (sensor_data.find("!") != -1):
                    set_brightness()
            except ValueError:
                pass

# This function will set screen brightness
def set_brightness():
    
    brightness_file = open(backlight_path + os.listdir(backlight_path)[0] + "/" + file_to_open, "w")
    brightness_file.write(str(constrain_sensor_values(int(sensor_data[:sensor_data.index("!")]), 10, get_max_brightness())))
    brightness_file.close()

    # FOR DEBUG
    #print sensor_data[:sensor_data.index("!")]


try:
    main()
except KeyboardInterrupt:
    print "\nExiting... Good bye! ;)"
    sys.exit()
except IOError as err:
    if (err.errno == 13):   # "Permission denied" error
        print "This script must be run as root!"
        sys.exit()
