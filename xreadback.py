# ********************************************************************************************
# ********************************************************************************************
#
#		Name: 		xreadback.py
#		Author:		Paul Robson (paul@robsons.org.uk)
#		Purpose:	Convert joystick button presses to GUI mouse clicks
#		Date:		31th July 2020
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
#								Event Source class
#
# ********************************************************************************************

class EventSources(object):
	def __init__(self):
		if not EventSources.isInitialised:											# Only initialise SDL once
			self.initialiseSDL()
			self.joystick = None if SDL_NumJoysticks()==0 else SDL_JoystickOpen(0)	# See if joystick available
			if self.joystick is not None:
				print("Found joystick")
	#
	#		Initialise SDL and Joystick subsystem
	#
	def initialiseSDL(self):
		SDL_Init(SDL_INIT_JOYSTICK)
		EventSources.isInitialised = True
	#
	#		Close down.
	#
	def close(self):
		if EventSources.isInitialised:
			SDL_JoystickClose(self.joystick)
			SDL_Quit();
			EventSources.isInitialised = False
	#
	#		Track button events and fire accordingly
	#
	def run(self,buttonHandlerList = []): 						
		assert EventSources.isInitialised											# check running SDL
		running = True							
		event = SDL_Event()
		self.listener = keyboard.Listener(
    		on_press=self.on_press)
		self.listener.start()
		while running:																# we *might* break out but probably won't.
			while SDL_PollEvent(ctypes.byref(event)) != 0: 							# don't seem to have button-down events.
				if event.type == SDL_QUIT:
					running = False
				if event.type == SDL_JOYBUTTONDOWN:									# pass on button events.
					self.eventHandler("B:"+str(event.jbutton.button))
				#
			time.sleep(0.1)															# check 10 times a second, don't go mad.
	#
	#		Handles presses
	#			
	def on_press(self,key):
		try:
			ch = key.char
		except AttributeError:
			ch = str(key)
			ch = ch[4:] if ch.startswith("Key.") else ch
		self.eventHandler("K:"+ch.lower())
	#
	#		Dummy event handler
	#
	def eventHandler(self,evType):
		print("** Fired Event '{0}' **".format(evType))

EventSources.isInitialised = False 

EventSources().run()