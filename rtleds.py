"""
rtleds 1.0 

API designed to access User LEDs in NI Linux Real-Time devices
    +Developed in Python 3.12.7 ->  Supported
    +tested in Python 3.10.14   ->  Supported
    +tested in Python 3.10.6    ->  Supported
    +tested in Python 3.5.5     ->  Supported


Supported models: cRIO-903X/904X/905X/906X, SbRIO-962X, RT PXIe controllers (only tested in PXIe-8880), RT cDAQ controllers (only tested in cDAQ-9134)
Not supported models: RoboRIO(1&2), MyRIO-1900/1950, ELVIS(I,II,III), cRIO-902X/907X/908X
Not tested models: SbRIO-9656/963X/960X, rest of RT PXIe controllers, rest of RT cDAQ-913X controllers

"""
# Importing required module
from sys import exit
import os

#Print available user LEDs in current NI Linux RT device ***************

def PrintTargetLEDs():
    #Search LEDs brightness files
    LEDs = os.popen('find /sys/devices -type f -name brightness | grep -i leds/nilrt:').read()
    LEDs = LEDs.splitlines()
    #Get LEDs common path
    common_path = os.path.commonprefix(LEDs)
    #Filter RT target user LEDs
    userLEDs = {"user0":['OFF'],"user1":['OFF'], "user2":['OFF'], "user3":['OFF']}
    colors = ["red","green","yellow"]
    #Search user match in path
    for key in userLEDs.keys():
        #Search color match in path
        for path in LEDs:
            if key in path:
                for color in colors:
                    if color in path:
                        userLEDs[key].append(color)
                        break
    #Print Results          
    for key in userLEDs.keys():
        if len(userLEDs[key]) > 1:
            print("{} >> {}".format(key,userLEDs[key]))

# USER LEDs CLASS ******************************************************

class RT_LED:

    def __init__(self):
        """
            Initialize LED class attributes
        """
        self.values = {0:"off",1:"green",2:"yellow"}
        self.value = 0
        self.led = ""
        self.leds_path = self._GetLEDsPath()

    def __call__(self, value):
        """
            Change RT LED status on each isntance call
        """
        if value == 0:
            self._TurnOFF()
        else:
            self._ChangeStatus(value)

    #PRIVATE --------------------------------------------------------

    def _GetLEDsPath(self):
        """
            Search and saves RT LEDs files location in the RT OS
        """
        #Look for brightness files related to RT target LEDs
        BrightnessPath = os.popen('find /sys/devices -type f -name brightness').read()
        BrightnessPath = BrightnessPath.splitlines()
        #Return common directory of user LEDs 
        LEDsPath = []
        for pad in BrightnessPath:
            if pad.find("leds/nilrt:") != -1:
                LEDsPath.append(pad)
        return os.path.commonprefix(LEDsPath)

    def _ValidateValue(self, value):
        """
            Validates input value is supported on RT target
        """
        val = self.values.get(value, "0")
        try:
            if isinstance(self, PXIe_user1) or isinstance(self, PXIe_user2):
                #Build path for PXIe targets
                path = "{}{}:{}/brightness".format(self.leds_path,val,self.led)
            else:
                #Build path for RIO targets
                path = "{}{}:{}/brightness".format(self.leds_path,self.led,val)        
            #Read file to validate correct LED color
            file = open(path, "r")
            file.close()
        #Error Handling xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        except:
            if value < 0 or value > 2:
                #print(f'Selected value is out of defined colors <{value}>, please select a valid color: 0->OFF 1->GREEN 2->YELLOW')
                print("Selected value is out of defined colors <{}>, please select a valid color: 0->OFF 1->GREEN 2->YELLOW".format(value))
            else:
                #print(f'The RT target does not support <{self.values[value]}> color in LED <{self.led}>')
                print("The RT target does not support <{}> color in LED <{}>".format(self.values[value],self.led))
            exit()
        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    def _ValidateLED(self):
            try:
                """
                    Verify whether class is for PXIe or RIO device
                """
                if isinstance(self, PXIe_user1) or isinstance(self, PXIe_user2):
                    #Build path file for PXIe targets
                    led_path = "{}green:{}/brightness".format(self.leds_path,self.led)
                else:
                    #Build path for RIO targets
                    led_path = "{}{}:green/brightness".format(self.leds_path,self.led)
                #Read file to validate correct LED color
                file = open(led_path, "r")
                file.read()
                file.close()
            #Error Handling xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
            except:
                print("This RT target does not support LED <{}>".format(self.led))
                exit()
            #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    
    def _TurnOFF(self):
        """
            Turns off both GREEN and YELLOW values of selected LED
        """
        if isinstance(self, PXIe_user1) or isinstance(self, PXIe_user2):
            #Build path for PXIe targets
            g_path = "{}green:{}/brightness".format(self.leds_path,self.led)
            y_path = "{}yellow:{}/brightness".format(self.leds_path,self.led)
        else:
            #Build path for RIO targets
            g_path = "{}{}:green/brightness".format(self.leds_path,self.led)
            y_path = "{}{}:yellow/brightness".format(self.leds_path,self.led)
        
        #Turn OFF green and yellow colors of selected LED
        leds = [g_path, y_path]
        for led_path in leds:
            try:
                #print(led_path)
                file = open(led_path, "w")
                file.write("0")
                file.close()
            except:
                pass
            
    def _ChangeStatus(self, value):
        """
            Updates selected LED status: OFF GREEN YELLOW
        """
        #Validate input LED color value
        self._ValidateValue(value)
        if isinstance(self, PXIe_user1) or isinstance(self, PXIe_user2):
            #Build path for PXIe targets
            led_path = "{}{}:{}/brightness".format(self.leds_path,self.values[value],self.led)
        else:
            #Build path for RIO targets
            led_path = "{}{}:{}/brightness".format(self.leds_path,self.led,self.values[value])
        #print(led_path)
        file = open(led_path, "w")
        file.write("1")
        file.close()

#INHERITED CLASSES *******************************************************

class RIO_user1(RT_LED):
    def __init__(self):
        super().__init__()
        self.led = "user1"
        self._ValidateLED()

    def __call__(self, value):
        return super().__call__(value)
    
class RIO_user2(RT_LED):
    def __init__(self):
        super().__init__()
        self.led = "user2"
        self._ValidateLED()

    def __call__(self, value):
        return super().__call__(value)

class PXIe_user1(RT_LED):
    def __init__(self):
        super().__init__()
        self.led = "user1"
        self._ValidateLED()

    def __call__(self, value):
        return super().__call__(value)

class PXIe_user2(RT_LED):
    def __init__(self):
        super().__init__()
        self.led = "user2"
        self._ValidateLED()

    def __call__(self, value):
        return super().__call__(value)

    