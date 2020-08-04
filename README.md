# xreadback

An attempt to sort out the XPlane 11 default ATC Readback issue, whereby you have to click readback 
messages with the mouse. Unless you are close to ambidextrous that means you have to let go of the 
joystick in order to grab the mouse to move and click it. For rookies like me flying by hand this is
often a problem. (It is a mystery why this has not been fixed. The default ATC isn't great, but this
makes it so much less irritating).

Installation
============

This has been designed to be cross platform but has only been run on Linux. It may simply not work
on Windows/Mac. The best way to find out is to just try it without XPlane first, clicking on things on the
desktop like icons or menus. It should give a commentary on what's happening in the command prompt.
Please feed back any issues !

Python3 programming language
	(from https://www.python.org/downloads/)
	When installing python click the checkbox to 'add to PATH'

Open a command prompt and install the following Python libraries.

Each should display some progress information and end with "Successfully installed" or
something like that.

pysdl2 Python library
	(Install via "pip install pysdl2")

sdl2 library
	(For Linux, often present or available in installer)
	(For Mac/Windows install with "pip install pysdl2-dll")

pynput Python library
	(Install via "pip install pynput")

If you get errors try adding a -U "pip install -U pynput"

Usage
=====

The app is very simple. Keyboard presses and Joystick button presses are checked against a
list. If a match is found, the mouse cursor is moved to a position on the screen and the left
mouse button is clicked.

(The obvious target is the top menu entry on ATC, which is sometimes "Readback Transmission")

This means that the ATC dialogue will have to be in a specific place and stay there. There 
probably is a way internally of figuring out where it is, but I have no idea how.

Probably it is best to anchor it to a side. I tend to have it at the bottom left.

The app is run at a terminal or command prompt.

To see the keyboard and joystick button names try the following:

python xreadback.py events

When a button or key is pressed it will show ** Fired Event 'xxxx' ** where xxxx is the name
of the event, e.g. k:x is the x key, and b:1 is button #1. (Interrupt it with control C)

Joystick buttons do not seem to work on complex setups. I don't know why. Changing 
SDL_JoystickOpen(0) currently at line 54 to different numbers might help, but we haven't 
managed to get this to work.

To see the mouse position try the following

python xreadback.py mouse

This just prints the current mouse position in the window, as you move it around you will see
the numbers change. Move it to where you want to click and make a note of that screen position.

Now suppose you want button 4 to do the readback, and the centre of the readback button is at
146,810. You would run the app with :

python xreadback.py b:4,146,810

This makes button 4 move the mouse cursor to 146,810 and click it. It will click whatever is at that
location. It's really for in flight, where you may not want to take your hands off the smaller planes 
controls at the time, it's especially irritating when it's just to acknowledge a change of heading.

To make the space bar do the same thing

python xreadback.py k:space,146,810

Just leave it running in the background while you run X-Plane. It shouldn't take up many resources.

Notes: 

1) these are physical screen positions, so if you run it in Windowed mode and move it about it will 
depend where the window is. The top left of the screen is 0,0

2) The install is not trivial. However, this is a good thing. This program is effectively what is called
a "key logger". It monitors what keys you press. The problem with such programs is that you could modify it
to write all the keys you press to a file, which mean passwords could be stolen as you type them in.

Because you can "see" the program in its original programmer form, it is possible to check this does not
do this.

Paul Robson, August 2020
paul@robsons.org.uk

Many thanks to Mark Smolen who helped with Windows testing and several attempts to try to make it work on
complex setups.
