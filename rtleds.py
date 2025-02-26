"""rtleds 1.0 - Python 3.12.7

API designed to access LEDs NI Linux Real-Time devices

"""
# Importing required module
import os

def match_1string_pattern(in_text,pattern):
    parts = in_text.split(pattern)

    try:
        before_match = parts[0]
    except:
        before_match = ""
    
    try:
        after_match = parts[1]
    except:
        after_match = ""

    return before_match, after_match

def SearchTarget_LEDs():
    LEDPaths = os.popen('find / -type f -name brightness').read()
    LEDPaths = LEDPaths.splitlines()

    common_prefix = os.path.commonprefix(LEDPaths)

    ls = []
    leds = []
    for pad in LEDPaths:
        _,af = match_1string_pattern(pad,"nilrt:")
        led,af = match_1string_pattern(af, ":")
        option,_ = match_1string_pattern(af,"/")
        
        if led in leds:
            ls[leds.index(led)].append(option)
        else:
            ls.append([option])
            leds.append(led)
        
        print(pad)

    LEDS = []
    print(LEDS)
    for l,o in zip(leds,ls):
        LEDS.append((l,o + ["off"]))

    print(LEDS)

    print("\nCommon prefix:", common_prefix)

    return common_prefix

class MyFunction:
    def __init__(self):
        self.counter = 0
    
    def count(self):
        self.counter += 1
        return self.counter

    