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
from sdl2 import *

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
			time.sleep(0.2)																# check 5 times a second, don't go mad.
			for h in buttonHandlerList:													# for each handler
				newState = SDL_JoystickGetButton(self.joystick,h.getButton()) != 0 		# get the new state of the button
				if newState != buttonStates[h.getButton()]:								# state changed ?
					buttonStates[h.getButton()] = newState 								# update it
					if newState:														# on button down
						h.fireButton()													# fire it.
	#
	#		Make identifying buttons easy. Prints buttons when pressed.
	#
	def test(self):
		event = SDL_Event()
		while True:
			while SDL_PollEvent(ctypes.byref(event)) != 0: 								# Message pump
				if event.type == SDL_QUIT:
					running = False
			for n in range(0,32):														# Scan and print pressed buttons
				if SDL_JoystickGetButton(self.joystick,n) != 0:
					print("Button {0} pressed.".format(n))
			print()

JoystickButtons.isInitialised = False		

# ********************************************************************************************
#
#										Test class
#
# ********************************************************************************************

class ButtonHandlerTest(object):
	def __init__(self,button):
		self.button = button
	def getButton(self):
		return self.button
	def fireButton(self):
		print("Fired ",self.button)

jb = JoystickButtons()
jb.test()
jb.run([ButtonHandlerTest(1),ButtonHandlerTest(2),ButtonHandlerTest(3)])
