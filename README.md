# rtleds 1.0
Python API designed to access User LEDs in NI Linux Real-Time (RT) devices.

### Supported Python versions
- Developed in Python 3.12.7 ->  Supported
- Tested in Python 3.10.14   ->  Supported
- Tested in Python 3.10.6    ->  Supported
- Tested in Python 3.5.5     ->  Supported

> Note: Rest of available Python versions in NI Linux RT controllers were not tested, but should work if they are later than 3.5.5

### Supported NI Linux Real-Time models: 
- cRIO-903X
- cRIO-904X
- cRIO-905X
- cRIO-906X
- SbRIO-9603/6907/9608/9609
- SbRIO-9627/9628/9629
- SbRIO-9637/9638
- PXIe Controllers
- cDAQ Controllers cDAQ-9132/9133/9134/9135/9136/9137
- Industrial Controllers IC-312X/317X
- Compact Vision Systems CVS-1458/1459

### Not supported models
- RoboRIO(1,2)
- MyRIO-1900/1950
- ELVIS(I,II,III)
- VxWorks OS Controllers (cDAQ, PXIe, cRIO, SbRIO)
- Pharlap OS Controllers (cDAQ, PXIe, cRIO, SbRIO)
- cDAQ Controllers cDAQ-9138/9139
- Compact Vision Systems CVS-1454/1455/1456/1457
- Compact Field Point (cFP) Controllers
- Smart Camera NI-17XX
- Monochrome/Color Smart Camera ISC-178X

> Note: Only NI Linux RT controllers (Intelx64 and ARM based) support this API, you can take a look at [Real-Time Controllers and Real-Time Operating System Compatibility][NI-Linux-RT-OS-Compatibility] to confirm compatibility.

# Using the API

#### Discovering Available User LEDs and Colors

If you do not know how many user LEDs your NI Linux RT controller has, and how many colors are supported you can run the following snippet to know it:
```sh
import rtleds
rtleds.PrintTargetLEDs()
```
This is the result for a PXIe-8880 with NI Linux RT:
```sh
user1 >> ['OFF', 'yellow', 'green']
user2 >> ['OFF', 'yellow', 'green']
```
> Note: If the current RT target does not have user LEDs you will get the following message `This target does not support User LEDs`.

#### Configuring LEDs

You can configure user LEDs `1` or `2`, to one of their possible colors `green` or `yellow`.

##### RIO controllers (cDAQ, cRIO, SbRIO)

```sh
#Create user LED1 object
usrled = rtleds.RIO_user1()
#Create user LED2 object
usrled = rtleds.RIO_user2()
```

##### PXIe controllers

```sh
#Create user LED1 object
usrled = rtleds.PXIe_user1()
#Create user LED2 object
usrled = rtleds.PXIe_user2()
```
> Note: Not all the NI Linux RT controllers have user2 LED. If they do not support `user2 LED` you will get the following message `This RT target does not support LED <n>`

#### Setting values to LEDs
Once created your LEDs objects you can set their value by calling the same instance of your LED object.
- `0` to turn OFF
- `1` to turn GREEN
- `2` to turn YELLOW

The example below turns ON and then OFF the `user2` LED `yellow` of a PXIe-8880.
```sh
import rtleds
#Create user2 LED instance
usrled = rtleds.PXIe_user2()
#Turn ON yellow user2 LED
usrled(2)
#Turn OFF user2 LED
usrled(0)
```
> Note: Not all the user LEDs support `yellow` color. If they do not support it you will get one of the following messages `Selected value is out of defined colors <n>, please select a valid color: 0->OFF 1->GREEN 2->YELLOW"` or `The RT target does not support <n> color in LED <n>`

[//]: # (Referenced Links)

[NI-Linux-RT-OS-Compatibility]: <https://www.ni.com/en/support/documentation/compatibility/17/real-time-controllers-and-real-time-operating-system-compatibili.html>




