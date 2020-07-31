from pygame.locals import *
import pygame

pygame.init()

finished = False

while not finished:
	for event in pygame.event.get():
		print(str(event))
		if event.type == pygame.QUIT:
			finished = True
		if event.type == pygame.KEYDOWN:
			print(event.type)