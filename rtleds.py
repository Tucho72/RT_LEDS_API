"""
rtleds 1.0 - Python 3.12.7

API designed to access User LEDs in NI Linux Real-Time devices

"""
# Importing required module
import os

def Match1StringPattern(in_text,pattern):

    """
        Search a single match pattern in the input string,
        and returns the string splitted before and after the match
    """
    parts = in_text.split(pattern,1)

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
        _,af = Match1StringPattern(pad,"nilrt:")
        led,af = Match1StringPattern(af, ":")
        option,_ = Match1StringPattern(af,"/")
        
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

class RT_LED:
    def __init__(self):
        self.leds_path = self._GetLEDsPath()
        self.values = {0:"off",1:"green",2:"yellow"}
        self.led = ""
        self.value = 0

    def _GetLEDsPath(self):
        """
            Search and saves RT LEDs files location in the RT OS
        """
        LEDPaths = os.popen('find / -type f -name brightness').read()
        LEDPaths = LEDPaths.splitlines()
        return os.path.commonprefix(LEDPaths)

    def __call__(self, led,value):
        led.lower()
        try:
            if value == 0:
                print(f"turned OFF {led} : green & yellow")
            else:
                path = f"{self.leds_path}{led}:{self.values.get(led, "OFF")}/brightness"
                print(path)
            # Open the file in read mode
            file = open(path, "r")
            # Read the entire content of the file
            content = file.read()
            # Print the content
            print(content)
            # Close the file
            file.close()
            print("valid LED")
        except:
            if led != "user1" and led != "user2":
                print(f"Wrong LED selected. Please enter a valid user LED: user1, user2")
            elif value in range(0,2):
                print(f"The RT target does not support <{self.values[value]}> color in LED <{led}>")
            else:
                print("Selected value is out of defined colors, please select a valid color: 0->OFF 1->GREEN 2->YELLOW")
                    

    def count(self):
        self.counter += 1
        return self.counter

    