"""
rtleds 1.0 - Python 3.12.7

API designed to access User LEDs in NI Linux Real-Time devices

"""
# Importing required module
import os

class RT_LED:
    def __init__(self):
        self.leds_path = self._GetLEDsPath()
        self.values = {0:"off",1:"green",2:"yellow"}
        self.led = ""
        self.value = 0

    #PRIVATE --------------------------------------------------------
    def _GetLEDsPath(self):
        """
            Search and saves RT LEDs files location in the RT OS
        """
        LEDPaths = os.popen('find / -type f -name brightness').read()
        LEDPaths = LEDPaths.splitlines()
        return os.path.commonprefix(LEDPaths)

    def __call__(self, led, value):
        """
            Change RT LED status on each isntance call
        """
        led.lower()
        try:
            #Validate selected LED and value
            if value == 0:
                print(f"turned OFF {led} : green & yellow")
            else:
                path = f"{self.leds_path}{led}:{self.values.get(value, "OFF")}/brightness"
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

        #Error Handling xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        except:
            if led != "user1" and led != "user2":
                print(f"Wrong LED selected. Please enter a valid user LED: user1, user2")
            elif value < 0 or value > 2:
                print(f"Selected value is out of defined colors <{value}>")
                print("please select a valid color: 0->OFF 1->GREEN 2->YELLOW")
            else:
                print(f"The RT target does not support <{self.values[value]}> color in LED <{led}>")
                
        #Error Handling xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
           
    #PUBLIC --------------------------------------------------------
    def count(self):
        self.counter += 1
        return self.counter

    