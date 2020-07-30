# ********************************************************************************************
# ********************************************************************************************
#
#		Name: 		xreadback.py
#		Author:		Paul Robson (paul@robsons.org.uk)
#		Purpose:	Convert joystick button/keyboard presses to GUI mouse clicks
#		Date:		26th July 2020
#
# ********************************************************************************************
# ********************************************************************************************

import sys
import ctypes
import time
import re
from inputs import *
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
	#
	#		Test mouse controller.
	#
	def test(self):
		while True:
			print("Mouse cursor at ",self.getPosition())

# ********************************************************************************************
#
#							  Event Handler Base Class
#								 (also wraps pysdl2)
#
# ********************************************************************************************

class EventSource(object):

	def run(self,handlers):
		self.handlers = handlers
		self.poll()

	def test(self):
		self.run([])

	def poll(self):
		self.handlerHash = {}
		for h in self.handlers:
			self.handlerHash[h.getButton()] = h
		while True:
			events = self.getEvents()												# get events
			if events:																# filter and send them.
				for e in events:
					if e.ev_type == "Key" and e.state != 0:
						self.fireEvent(e.code.lower())
		time.sleep(0.1)																# check 10 times a second, don't go mad.

	def fireEvent(self,key):
		print("Event:",key)
		if key in self.handlerHash:
			print("Firing:",key)
			self.handlerHash[key].fireButton()


class KeyEventSource(EventSource):
	def getEvents(self):
		return get_key()													

class ButtonEventSource(EventSource):
	def getEvents(self):
		try:
			events = get_gamepad()													
		except UnknownEventCode:
			print("Warning:Not a definable button.")
			events = None
		return events

# ********************************************************************************************
#
#									Test Handler class
#
# ********************************************************************************************

class TestHandler(object):
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
		print("Move and click:",self.button)
		self.mouseController.move(self.x,self.y)
		self.mouseController.click()
	#
	#		Convert string list to list of integers, mouse definition
	#
	def makeList(self,defn):
		defn = defn.replace(" ","").replace("\t"," ")
		m = re.match("^(.*?)\\,(\\d+)\\,(\\d+)$",defn) 
		assert m is not None,"Bad definition "+defn
		return [m.group(1).strip().lower(),int(m.group(2)),int(m.group(3))]

if len(sys.argv) == 1:
	print("xreadback v0.2 by Paul Robson paul@robsons.org.uk. MIT Licensed.")
	print("\txreadback mouse|buttons|keys - display mouse pos, pressed buttons,pressed keys")
	print("\txreadback event,x,y event,x,y - map events button to click at x,y ")
	print("\tfor example : xreadback btn_trigger,56,16")
	sys.exit(0)

mc = MouseController()

if len(sys.argv) == 2:
	param2 = sys.argv[1].lower().strip() 
	if param2 == "mouse":
		mc.test()
	elif param2 == "keys":
		KeyEventSource().test()
	elif param2 == "buttons":
		ButtonEventSource().test()

handlers = []
for i in range(1,len(sys.argv)):
	handlers.append(ClickButtonHandler(sys.argv[i],mc))
	assert handlers[0].getButton()[:3] == handlers[-1].getButton()[:3],"Cannot mix joystick buttons/keys"

source = KeyEventSource() if handlers[0].getButton()[:3] == "key" else ButtonEventSource()

source.run(handlers)
