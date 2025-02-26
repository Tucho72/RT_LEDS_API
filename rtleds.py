"""
rtleds 1.0 
    +Developed in Python 3.12.7
    +tested in Python 3.10.14   ->    Supported
    +tested in Python 3.10.6    ->     Supported
    +tested in Python 3.5.5     ->      Supported

API designed to access User LEDs in NI Linux Real-Time devices

"""
# Importing required module
from sys import exit
import os

class RT_LED:

    def __init__(self):
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
        LEDPaths = os.popen('find / -type f -name brightness').read()
        LEDPaths = LEDPaths.splitlines()
        return os.path.commonprefix(LEDPaths)

    def _ValidateValue(self, value):
        #Validate selected LED and value
            try:
                #Build LED path file
                val = self.values.get(value, 0)
                #path = f'{self.leds_path}{self.led}:{val}/brightness'
                path = "{}{}:{}/brightness".format(self.leds_path,self.led,val)        
                # Open and read LED status path 
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
            #Error Handling xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    def _ValidateLED(self):
            try:
                #led_path = f'{self.leds_path}{self.led}:green/brightness'
                led_path = "{}{}:green/brightness".format(self.leds_path,self.led)
                print(led_path)
                file = open(led_path, "r")
                file.read()
                file.close()
            except:
                #print(f'This RT target does not support LED <{self.led}>')
                print("This RT target does not support LED <{}>".format(self.led))
                exit()
            # This method should be implemented by subclasses
            #raise NotImplementedError("Subclasses must implement this method")
    
    def _TurnOFF(self):
        #Build Green input LED path file
        #g_path = f'{self.leds_path}{self.led}:green/brightness'
        #y_path = f'{self.leds_path}{self.led}:yellow/brightness'
        g_path = "{}{}:green/brightness".format(self.leds_path,self.led)
        y_path = "{}{}:yellow/brightness".format(self.leds_path,self.led)
        leds = [g_path, y_path]
        #Turn OFF green and yellow colors of selected LED
        for led_path in leds:
            try:
                print(led_path)
                file = open(led_path, "w")
                file.write("0")
                file.close()
            except:
                pass
            
    def _ChangeStatus(self, value):
        print("Changing value")
        self._ValidateValue(value)

        #led_path = f'{self.leds_path}{self.led}:{self.values[value]}/brightness'
        led_path = "{}{}:{}/brightness".format(self.leds_path,self.led,self.values[value])
        print(led_path)
        file = open(led_path, "w")
        file.write("1")
        file.close()

#INHERITED CLASSES *******************************************************

class USER1(RT_LED):
    def __init__(self):
        super().__init__()
        self.led = "user1"
        self._ValidateLED()

    def __call__(self, value):
        return super().__call__(value)
    
class USER2(RT_LED):
    def __init__(self):
        super().__init__()
        self.led = "user2"
        self._ValidateLED()

    def __call__(self, value):
        return super().__call__(value)



    