# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
`fingerprint_template_file_compare.py`
====================================================

This is an example program to demo storing fingerprint templates in a file. It also allows
comparing a newly obtained print with one stored in the file in previous step. This is helpful
when fingerprint templates are stored centrally (not on sensor's flash memory) and shared
between multiple sensors.

* Author(s): admiralmaggie

Implementation Notes
--------------------

**Hardware:**

* `Fingerprint sensor <https://www.adafruit.com/product/751>`_ (Product ID: 751)
* `Panel Mount Fingerprint sensor <https://www.adafruit.com/product/4651>`_ (Product ID: 4651)
"""


import serial
import adafruit_fingerprint
import os


# import board (if you are using a micropython board)
# uart = busio.UART(board.TX, board.RX, baudrate=57600)

# If using with a computer such as Linux/RaspberryPi, Mac, Windows with USB/serial converter:
#uart = serial.Serial("COM6", baudrate=57600, timeout=1)

# If using with Linux/Raspberry Pi and hardware UART:
uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

# If using with Linux/Raspberry Pi 3 with pi3-disable-bte
# uart = serial.Serial("/dev/ttyAMA0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

directory = './finger_prints/'
if not os.path.exists(directory):
    os.makedirs(directory)

##################################################


def sensor_reset():
    """Reset sensor"""
    print("Resetting sensor...")
    if finger.soft_reset() != adafruit_fingerprint.OK:
        print("Unable to reset sensor!")
    print("Sensor is reset.")


# pylint: disable=too-many-branches
def fingerprint_check_file(stu_num):
    """Compares a new fingerprint template to an existing template stored in a file
    This is useful when templates are stored centrally (i.e. in a database)"""
    print("Waiting for finger print...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False

    print("Loading file template...", end="")
    with open(f'{directory}template_{stu_num}.dat', "rb") as file:
        data = file.read()
    finger.send_fpdata(list(data), "char", 2)

    i = finger.compare_templates()
    if i == adafruit_fingerprint.OK:
        print("Fingerprint match template in file.")
        return True
    if i == adafruit_fingerprint.NOMATCH:
        print("Templates do not match!")
    else:
        print("Other error!")
    return False
    
def fingerprint_check_by_recieved(stu_id):
    """Compares a new fingerprint template to an existing template stored in a file
    This is useful when templates are stored centrally (i.e. in a database)"""
    print("Waiting for finger print...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False

    print("Loading file template...", end="")
    with open(f'./recievedTamplet/{stu_id}.dat', "rb") as file:
        data = file.read()
    finger.send_fpdata(list(data), "char", 2)

    i = finger.compare_templates()
    if i == adafruit_fingerprint.OK:
        print("Fingerprint match template in file.")
        return True
    if i == adafruit_fingerprint.NOMATCH:
        print("Templates do not match!")
    else:
        print("Other error!")
    return False


# pylint: disable=too-many-statements
def enroll_save_to_file(stu_num):
    attempt_counter = 0  # 시도 횟수를 저장하는 변수

    while attempt_counter < 3:  # 시도 횟수가 3번 미만인 동안 반복
        attempt_counter += 1  # 시도 횟수 증가

        for fingerimg in range(1, 3):
            if fingerimg == 1:
                print("Place finger on sensor...", end="")
            else:
                print("Place same finger again...", end="")

            while True:
                i = finger.get_image()
                if i == adafruit_fingerprint.OK:
                    print("Image taken")
                    break
                if i == adafruit_fingerprint.NOFINGER:
                    print(".", end="")
                elif i == adafruit_fingerprint.IMAGEFAIL:
                    print("Imaging error")
                    return False
                else:
                    print("Other error")
                    return False

            
            print("Templating...", end="")
            i = finger.image_2_tz(fingerimg)
            if i == adafruit_fingerprint.OK:
                print("Templated")
            else:
                if i == adafruit_fingerprint.IMAGEMESS:
                    print("Image too messy")
                elif i == adafruit_fingerprint.FEATUREFAIL:
                    print("Could not identify features")
                elif i == adafruit_fingerprint.INVALIDIMAGE:
                    print("Image invalid")
                else:
                    print("Other error")
                return False

            if fingerimg == 1:
                print("Remove finger")
                while i != adafruit_fingerprint.NOFINGER:
                    i = finger.get_image()

        print("Creating model...", end="")
        i = finger.create_model()
        if i == adafruit_fingerprint.OK:
            print("Created")
        else:
            if i == adafruit_fingerprint.ENROLLMISMATCH:
                print("Prints did not match")
            else:
                print("Other error")
            continue  # 처음으로 돌아가기

        print("Downloading template...")
        data = finger.get_fpdata("char", 1)
        with open(f'{directory}template_{stu_num}.dat', "wb") as file:
            file.write(bytearray(data))
        print(f'Template is saved in template{stu_num}.dat file.')

        return True

    return False  # 3번 시도 후에도 실패할 경우 False 반환

