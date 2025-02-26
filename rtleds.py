"""rtleds 1.0 - Python 3.12.7

API designed to access LEDs NI Linux Real-Time devices

"""
 
# Importing required module
import os

def SearchTarget_LEDs():
    LEDPaths = os.popen('find / -type f -name brightness').read()
    LEDPaths = LEDPaths.splitlines()

    common_prefix = os.path.commonprefix(LEDPaths)

    for pad in LEDPaths:
        print(f'Path: {pad}')

    print("\nCommon prefix:", common_prefix)

    return common_prefix