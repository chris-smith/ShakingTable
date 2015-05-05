import Player
from PlayerGun import *
from HXMReceiver_M import *
from math import pi

class Player_M (Player.Player):

	def __init__ (self, containers, screen):
		Player.Player.__init__(self, containers, screen)
		
		#we're going to use a different hx receiver, so close down the default on and open up the new one
		#self.hxm.close()
		self.hxm = None
		self.hxm = HXMReceiver_M()
		self.hxm.run()

	def fire (self, stress=0):
		if self.hxm.bullets > 0:
			self.bullets.append(PlayerShot(
								self._x + self._bulletOffset, 
								(self._containers, self.bulletGroup), 
								self._screen, 
								angle=-(pi/180.)*self._wobbleAngle, 
								stress=0))
			self.hxm.bullets -= 1
	
	def draw (self):
		Sprite.draw(self)
		for bullet in self.bullets:
			bullet.draw()