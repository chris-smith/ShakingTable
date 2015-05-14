import pygame, numpy, sys, os
from pygame.locals import *
from Sprite import *
from math import sin, cos
from random import uniform
from Sounds import *

mainDir = os.path.split(os.path.abspath(__file__))[0]
bulletSpeed=10.
particleSpeed=10.
bulletVelocity=numpy.array([0., -5.])
maxParticles = 20
alphaDecay = 0.1

class PlayerShot (Sprite):

	def __init__ (self, loc, containers, screen, sound_on=True, angle=0., stress=0.):
		_v = numpy.array([sin(angle), -cos(angle)]) * bulletSpeed
		self._particles = []
		_a = numpy.zeros(2)
		if stress > 0:
			_a[1] = 1.
		else:
			if (sound_on):
				Sounds().Fire()
		Sprite.__init__(self, containers, screen, imageFile='star.jpg', size=(20,20), x=loc, v=_v, a=_a)
		self._surface.set_colorkey((255,255,255))
	
	def move (self):
		Sprite.move(self)
		if (len(self._particles) < maxParticles):
			self.addParticle()
		for particle in self._particles:
			if particle.alpha <= 0:
				self._particles.remove(particle)
			else:
				particle.move()
				
	def addParticle (self):
		self._particles.append(PlayerShotParticle(self._x.copy(), self._containers, self._screen))
		
	def draw (self):
		Sprite.draw(self)
		for particle in self._particles:
			particle.draw()

class PlayerShotParticle (Sprite):

	def __init__ (self, loc, containers, screen, alpha=1.):
		v0 = numpy.array([random.uniform(-0.25,0.25), 0])
		v1 = v0 * particleSpeed
		Sprite.__init__(self, containers, screen, imageFile='star.jpg', size=(20,20), x=loc, v=v1)
		self.alpha = alpha
		self._surface.set_colorkey((255,255,255))
		self.kill()	# particle don't get to be in any group
	
	def move (self):
		Sprite.move(self)
		self._surface.set_alpha(255.*self.alpha)
		self.alpha -= alphaDecay