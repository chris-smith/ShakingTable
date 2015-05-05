import sys, pygame, os
from pygame.locals import *
import pygame.mixer
from random import choice
from datetime import datetime, timedelta

_mainDir = os.path.split(os.path.abspath(__file__))[0]
_soundDir = 'Sounds'
_shotFileName = 'shot2.wav'
_explosionFileName = 'explosion.wav'
_entryFileNames = ['entry1.wav','entry2.wav','entry3.wav','entry4.wav']

lastStart = datetime.now() + timedelta(seconds=-3)

class Sounds:

	def __init__ (self):
		pygame.mixer.init()
		pygame.mixer.set_num_channels(32)
		self.fireSound = pygame.mixer.Sound(os.path.join(_mainDir, _soundDir, _shotFileName))
		self.explosionSound = pygame.mixer.Sound(os.path.join(_mainDir, _soundDir, _explosionFileName))
		self.entrySounds = []
		for file in _entryFileNames:
			self.entrySounds.append(pygame.mixer.Sound(os.path.join(_mainDir, _soundDir, file)))

	def Fire (self):
		self.fireSound.play()

	def VillianEntry (self):
		#print lastStart, datetime.now() - self.lastStart
		#if (datetime.now() - lastStart) > timedelta(seconds=3):
		#lastStart = datetime.now()
		#choice(self.entrySounds).play()
		return

	def Explode (self):
		self.explosionSound.play()
		