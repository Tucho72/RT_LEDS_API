import rtleds
import time

print("running main")

usrled = rtleds.RIO_user1()
#usrled = rtleds.PXIe_user1()

while(True):
#for i in range(0,5):
    usrled(1)
    time.sleep(0.2)
    print("LED ON")
    usrled(0)
    time.sleep(0.2)
    print("LED OFF")

print("END")




