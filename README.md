# xreadback
An attempt to sort out the XPlane 11 default ATC Readback issue

The issue being the absurd requirement to click readback messages with the mouse. Unless
you are close to ambidextrous that means you have to let go of the joystick in order to grab
the damn mouse to move and click it. 

However good the coders of XPlane may be, this is a remarkably stupid UI issue when most of the
messages are simply echoing. If they can't allocate a function to it, there should be an option to 
make readbacks automatic. 

Installation
============

This has been designed to be cross platform but has only been run on Linux. It may simply not work
on Windows/Mac. The best way to find out is to just try it without XPlane first, clicking on things on the
desktop like icons or menus. It should give a commentary on what's happening in the command prompt.
Please feed back any issues !

Python3 programming language
	(from https://www.python.org/downloads/)
	When installing python click the checkbox to 'add to PATH'

pysdl2 Python library
	(Install via "pip install -U pysdl2")

sdl2 library
	(For Linux, often present or available in installer)
	(For Mac/Windows install with "pip install -U pysdl2-dll")

pynput Python library
	(Install via "pip install -U pynput")

Usage
=====

The app is very simple. It scans the joystick buttons requested and when one is pressed it 
moves the mouse cursor to a specific position and clicks it. It can do this for as many 
places on the display as you like. 

(The obvious target is the top menu entry on ATC, which is sometimes "Readback Transmission")

This means that the ATC dialogue will have to be in a specific place and stay there. There 
probably is a way internally of figuring out where it is, but I have no idea how.

Probably it is best to anchor it to a side. I tend to have it at the bottom left.

The app is run at a terminal or command prompt.

To identify the buttons and get the position, do :

python xreadback.py test. 

This is incredibly rough and ready but shows you where the mouse cursor is, and what buttons 
are being pressed. (Interrupt it with control C)

Now suppose you want button 4 to do the readback, and the centre of the readback button is at
146,810. You would run the app with :

python xreadback.py 4,146,810

This makes button 4 move the mouse cursor to 146,810 and click it. It will click whatever is at that
location. It's really for in flight, where you may not want to take your hands off the smaller planes 
controls at the time, it's especially irritating when it's just to acknowledge a change of heading.

Notes: 

1) these are physical screen positions, so if you run it in Windowed mode and move it about it will 
depend where the window is.
2) the command prompt 

Paul Robson, July 2020

