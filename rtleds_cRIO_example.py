import rtleds
import time

""" This example turns toggles the user1 LED of a cRIO-9054 """

#Print available user LEDs in cRIO-9054
rtleds.PrintTargetLEDs()

#Create user1 object
usrled = rtleds.RIO_user1()

for i in range(0,5):
    usrled(1)
    time.sleep(0.2)
    print("LED ON")
    usrled(0)
    time.sleep(0.2)
    print("LED OFF")

print("END")




