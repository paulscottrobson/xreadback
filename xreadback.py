# ********************************************************************************************
# ********************************************************************************************
#
#		Name: 		xreadback.py
#		Author:		Paul Robson (paul@robsons.org.uk)
#		Purpose:	Convert joystick button presses to GUI mouse clicks (3rd version !)
#		Date:		4th August 2020
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
#								A wrapper for pynput mouse controller
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
		SDL_Init(SDL_INIT_JOYSTICK)													# start SDL, only Joystick.
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
		event = SDL_Event()															# events stored here
		self.listener = keyboard.Listener(	 										# on_press called for every
    		on_press=self.on_press)													# key press
		self.listener.start()
		while running:																# we *might* break out but probably won't.
			while SDL_PollEvent(ctypes.byref(event)) != 0: 							# don't seem to have button-down events.
				if event.type == SDL_QUIT:
					running = False
				if event.type == SDL_JOYBUTTONDOWN:									# pass on button events.
					self.eventHandler("b:"+str(event.jbutton.button))
				#
			time.sleep(0.1)															# check 10 times a second, don't go mad.
	#
	#		Handles presses
	#			
	def on_press(self,key):
		try:
			ch = key.char 															# the character
		except AttributeError:
			ch = str(key) 															# if it isn't one convert
			ch = ch[4:] if ch.startswith("Key.") else ch 							# to key name e.g. "shift"
		self.eventHandler("k:"+ch.lower()) 											
	#
	#		Dummy event handler
	#
	def eventHandler(self,evType):
		print("** Fired Event '{0}' **".format(evType))

# ********************************************************************************************
#
#					Event source class that actually runs the triggers
#
# ********************************************************************************************

class ExecEventSources(EventSources):
	#
	#		Subclass run to store event handlers
	#
	def run(self,eventHandlers):					
		self.eventHandlers = {} 													# save triggers to do
		for eh in eventHandlers:													# convert to a lookup dictionary
			self.eventHandlers[eh.getButton()] = eh
		EventSources.run(self)														# call superclass	
	#
	#		Override event handler
	#
	def eventHandler(self,evType):
		evType = evType.lower()
		if evType in self.eventHandlers:											# do we know this one ?
			print("Firing event ",evType)
			self.eventHandlers[evType].fireButton()									# yes, go do it.

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
		m = re.match("^(.*?)\\,(\\d+)\\,(\\d+)$",defn.strip())
		assert m is not None,"Bad definition "+defn
		return [m.group(1).strip().lower(),int(m.group(2)),int(m.group(3))]

EventSources.isInitialised = False 

if len(sys.argv) == 1:
	print("xreadback v0.3 by Paul Robson paul@robsons.org.uk. MIT Licensed.")
	print("\txreadback events - display key presses/joystick buttons as pressed")
	print("\txreadback mouse - display mouse cursor position")
	print("\txreadback event,x,y event,x,y - map button/key event to click at x,y ")
	sys.exit(0)

mouseCtrl = MouseController()

if len(sys.argv) == 2:
	cmd = sys.argv[1].lower()
	if cmd == "mouse":
		while True:
			print("Mouse position: ",mouseCtrl.getPosition())
	if cmd == "events":
		EventSources().run()

eventHandlers = []
for eDesc in sys.argv[1:]:
	eventHandlers.append(ClickButtonHandler(eDesc,mouseCtrl))

ExecEventSources().run(eventHandlers)
