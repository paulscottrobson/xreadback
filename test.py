# ********************************************************************************************
# ********************************************************************************************
#
#		Name: 		xreadback.py
#		Author:		Paul Robson (paul@robsons.org.uk)
#		Purpose:	Convert joystick button presses to GUI mouse clicks
#		Date:		29th July 2020
#
# ********************************************************************************************
# ********************************************************************************************

import sys
import ctypes
import time
import re
from sdl2 import *
from inputs import get_key
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
			self.joystick = None
			if SDL_NumJoysticks() > 0:													# Check joystick available
				self.joystick = SDL_JoystickOpen(0);									# Access the primary
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
	#		Track button and keyboard events 
	#
	def run(self): 						
		assert JoystickButtons.isInitialised											# check running SDL
		running = True							
		event = SDL_Event()
		while running:																	# we *might* break out but probably won't.
			while SDL_PollEvent(ctypes.byref(event)) != 0: 								# don't seem to have button-down events.		
				if event.type == SDL_QUIT:
					running = False
#				if event.type == SDL_JOYBUTTONDOWN:										# joystick button down ?
#					self.fireButtonEvent(event.jbutton.button)
			events = get_key()															# keyboard events occurred ?
			if events:																	# filter and send them.
				for e in events:
					if e.ev_type == "Key" and e.state != 0:
						self.fireKeyboardEvent(e.code[4:].lower())
			time.sleep(0.1)																# check 5 times a second, don't go mad.
	#
	#		Fire joystick button event
	#
	def fireButtonEvent(self,buttonID):
		print("Button pressed ",buttonID)
	#
	#		Fire keyboard event
	#
	def fireKeyboardEvent(self,keyID):
		print("Key pressed ",keyID)

JoystickButtons.isInitialised = False

jb = JoystickButtons()
jb.run()
