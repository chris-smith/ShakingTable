import pygame, numpy, sys, os, random
from math import fabs
from pygame.locals import *

_mainDir = os.path.split(os.path.abspath(__file__))[0]
_aether = numpy.array([0.01, 0.])
_accelDecay = numpy.array([0.5, 0.])
_maxRot = 45.
_maxWobbleAngle = 45.
_maxV = [20., 40.]
x = 0
y = 1

class Sprite (pygame.sprite.Sprite):
	
	def __init__ (self, 
					containers, 
					screen, 
					imageFile, 
					imageDir='art', 
					size = (50, 50), 
					x=numpy.array([0.,0.]), 
					v=numpy.array([0.,0.]),
					a=numpy.array([0.,0.]),
					wobble=0.,
					aether=_aether.copy(), 
					accelDecay=_accelDecay.copy()):
					
		pygame.sprite.Sprite.__init__(self, containers)
		self._containers = containers
		self._screen = screen
		boundX, boundY = screen.get_size()
		self._surface = pygame.transform.smoothscale(pygame.image.load(os.path.join(_mainDir, imageDir, imageFile)), size)
		sizeX, sizeY = self._surface.get_size()
		self._bounds = numpy.array([boundX-sizeX, boundY-sizeY])
		self._a = a
		self._v = v
		self._x = x
		self._wobble = wobble
		self._wobbleAngle = 0.
		self._aether = aether
		self._accelDecay = accelDecay
		self.rect = self._surface.get_rect()
	
	def getSize (self):
		return self._surface.get_size()
	
	def getCenter (self):
		offsetX, offsetY = self._surface.get_size()
		offsetX /= 2
		offsetY /= 2
		return self._x[x]+offsetX, self._x[y]+offsetY
	
	def draw (self):
		#rotate the surface for x-velocity
		s = pygame.transform.rotate(self._surface, -((self._v / _maxV)[x] * _maxRot))
		
		#rotate the surface for wobble
		s = pygame.transform.rotate(s, self._wobbleAngle)
		
		self._screen.blit(s, (self._x[0], self._x[1]))
		
	def move (self):
		#enforce the x-direction speed limit
		if (fabs(self._v[x]) > _maxV[x]):
			if (self._v[x] < 0):
				self._v[x] = -_maxV[x]
			else:
				self._v[x] = _maxV[x]
		
		#this is an aesthetic thing. If v[x] is very small, just make it 0, so it stops trying
		#rotate, which looks funny
		if (fabs(self._v[x]) < 0.3):
			self._v[x] = 0
			
		#deal with wobbling. This is usually used for a player that is stressed
		if (self._wobble):
			r = random.gauss(0., 3.)
			self._wobbleAngle += r
			if (fabs(self._wobbleAngle) > (_maxWobbleAngle * self._wobble)):
				if (self._wobbleAngle < 0):
					self._wobbleAngle = -(_maxWobbleAngle * self._wobble)
				else:
					self._wobbleAngle = (_maxWobbleAngle * self._wobble)
		
		self._v -= self._v * self._aether
		self._a -= self._a * self._accelDecay
			
		if (self._x[x] > self._bounds[x]) or (self._x[x] < 0):
			self._v[x] = self._v[x] * -1
			self._a[x] = self._a[x] * -1
		
		if (self._x[x] < 0):
			self._x[x]=0.
		if (self._x[x] > self._bounds[x]):
			self._x[x] = self._bounds[x]
		self._v += self._a
		self._x += self._v

	def bounce(self, collisionPos):
		# print "bouncing"
		self._v[x] = fabs(self._v[x] * 2)
		if(collisionPos > self._x[x]):
			self._v[x] = -self._v[x]

		