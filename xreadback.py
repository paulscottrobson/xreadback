# ********************************************************************************************
# ********************************************************************************************
#
#		Name: 		xreadback.py
#		Author:		Paul Robson (paul@robsons.org.uk)
#		Purpose:	Convert joystick button presses to GUI mouse clicks
#		Date:		26th July 2020
#
# ********************************************************************************************
# ********************************************************************************************

import sys
import ctypes
import time
import re
from sdl2 import *
from pynput import *

# ********************************************************************************************
#
#									A wrapper for pynput 
#
# ********************************************************************************************

class MouseController(object):
	def __init__(self):
		self.mouse = mouse.Controller()
	#
	#		Move mouse
	#
	def move(self,x,y):
		self.mouse.position = (x,y)
	#
	#		Click mouse left button
	#
	def click(self):
		self.mouse.click(mouse.Button.left, 1)
	#
	#		Get position
	#
	def getPosition(self):
		return self.mouse.position

# ********************************************************************************************
#
#							Joystick Button wrapper class
#								 (also wraps pysdl2)
#
# ********************************************************************************************

class JoystickButtons(object):
	def __init__(self):
		if not JoystickButtons.isInitialised:											# Only initialise SDL once
			self.initialiseSDL()
			assert SDL_NumJoysticks() > 0,"No joystick connected"						# Check joystick available
			self.joystick = SDL_JoystickOpen(0);										# Access the primary
			print("Found joystick")
	#
	#		Initialise SDL and Joystick subsystem
	#
	def initialiseSDL(self):
		SDL_Init(SDL_INIT_JOYSTICK)
		JoystickButtons.isInitialised = True
	#
	#		Close down.
	#
	def close(self):
		if JoystickButtons.isInitialised:
			SDL_JoystickClose(self.joystick)
			SDL_Quit();
			JoystickButtons.isInitialised = False
	#
	#		Track button events and fire accordingly
	#
	def run(self,buttonHandlerList = []): 						
		assert JoystickButtons.isInitialised											# check running SDL
		running = True							
		event = SDL_Event()
		buttonStates = {} 																# set initial states of buttons to false for each handler
		for h in buttonHandlerList:
			buttonStates[h.getButton()] = False
		while running:																	# we *might* break out but probably won't.
			while SDL_PollEvent(ctypes.byref(event)) != 0: 								# don't seem to have button-down events.
				if event.type == SDL_QUIT:
					running = False
			for h in buttonHandlerList:													# for each handler
				newState = SDL_JoystickGetButton(self.joystick,h.getButton()) != 0 		# get the new state of the button
				if newState != buttonStates[h.getButton()]:								# state changed ?
					buttonStates[h.getButton()] = newState 								# update it
					if newState:														# on button down
						h.fireButton()													# fire it.
			time.sleep(0.2)																# check 5 times a second, don't go mad.
	#
	#		Make identifying buttons easy. Prints buttons when pressed.
	#
	def test(self):
		event = SDL_Event()
		mc = MouseController()
		while True:
			while SDL_PollEvent(ctypes.byref(event)) != 0: 								# Message pump
				if event.type == SDL_QUIT:
					running = False
			for n in range(0,32):														# Scan and print pressed buttons
				if SDL_JoystickGetButton(self.joystick,n) != 0:
					print("Button {0} pressed.".format(n))
			print("Cursor at ",mc.getPosition())

JoystickButtons.isInitialised = False		

# ********************************************************************************************
#
#									Test Handler class
#
# ********************************************************************************************

class ButtonHandlerTest(object):
	def __init__(self,button):
		self.button = button
	def getButton(self):
		return self.button
	def fireButton(self):
		print("Fired ",self.button)

# ********************************************************************************************
#
#							Actual move/click handler class
#
# ********************************************************************************************

class ClickButtonHandler(object):
	def __init__(self,definition,mouseController):
		self.mouseController = mouseController
		if isinstance(definition,str):
			definition = self.makeList(definition)
		assert len(definition) == 3,"Bad mouse/button definition"
		print("Added definition Button {0} at {1},{2}".format(definition[0],definition[1],definition[2]))
		self.button = definition[0]
		self.x = definition[1]
		self.y = definition[2]
	#
	#		Get the button ID
	#
	def getButton(self):
		return self.button
	#
	#		Handle button being clicked.
	#
	def fireButton(self):
		print("Firing "+str(self.button))
		self.mouseController.move(self.x,self.y)
		self.mouseController.click()
	#
	#		Convert string list to list of integers, mouse definition
	#
	def makeList(self,defn):
		defn = defn.replace(" ","").replace("\t"," ")
		assert re.match("^\\d+\\,\\d+\\,\\d+$",defn) is not None,"Bad definition "+defn
		return [int(x) for x in defn.split(",")]

#jb.test()
#jb.run([ButtonHandlerTest(1),ButtonHandlerTest(2),ButtonHandlerTest(3)])

if len(sys.argv) == 1:
	print("xreadback v0.1 by Paul Robson paul@robsons.org.uk. MIT Licensed.")
	print("\txreadback test - display buttons as pressed")
	print("\txreadback b,x,y b,x,y - map joystick button to click at x,y ")
	sys.exit(0)

jb = JoystickButtons()
mc = MouseController()

if len(sys.argv) == 2 and sys.argv[1].lower().strip() == "test":
	jb.test()

buttonHandlers = []
for h in sys.argv[1:]:
	buttonHandlers.append(ClickButtonHandler(h,mc))	
jb.run(buttonHandlers)

#mc = MouseController()
#mc.move(146,800)
#	mc.click()