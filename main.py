import rtleds
import time

print("running main")

#usrled = rtleds.RIO_user2()
usrled = rtleds.PXIe_user1()

for i in range(0,5):
    usrled(2)
    time.sleep(1)
    usrled(0)
    time.sleep(1)
    
print("END")




