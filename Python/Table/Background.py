import pygame

class Background:

	def __init__(self, screen):
		self._background = pygame.Surface(screen.get_size())
		self._background = self._background.convert()
		self._background.fill((255, 255, 255))
		self._screen = screen
		self._screen.blit(self._background, (0,0))
		
	def draw(self):
		#print self._screen.get_size()

		self._screen.blit(self._background, (0,0))