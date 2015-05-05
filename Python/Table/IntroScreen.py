import pygame, Sprite, numpy, random, os

maxParticles = 150
particleSpeed = 15
alphaDecay = 0.025
black = (0,0,0)
red = (255,0,0)
white = (255,255,255)
_mainDir = os.path.split(os.path.abspath(__file__))[0]
_SoundImage = 'art/sound.jpg'
_MuteImage = 'art/sound_mute.png'
_SoundSize = (100,100)
_MuteSize = (50,100)

class IntroScreen:

	def __init__(self, screen):
		all = pygame.sprite.RenderUpdates()
		self._screen = screen
		# self.title = Sprite.Sprite(all, screen, imageFile='rage_title.png', size=(424,57), x=numpy.array([100.,100.]))
		self.titleParticles = Particles(all, screen, numpy.array([100.,100.]))
		self._PlayerFont = pygame.font.SysFont('Helvetica', 30, bold=True)
		self._TutorialFont = pygame.font.SysFont('Helvetica', 42, bold=True)
		self._SmallerFont = pygame.font.SysFont('Baskerville', 16, bold=False, italic=True)
		self._LargerFont = pygame.font.SysFont('Helvetica', 60, bold=True)
		self._TitleFont = pygame.font.SysFont('comicsansms',70,bold=True)
		self._TitlePos = (100,100)
		self._OnePlayerPos = (100,300)
		self._OnePlayerThresholdPos = (100,350)
		self._OnePlayerThresholdValPos = (100, 375)
		self._TwoPlayerPos = (400,300)
		self._TwoPlayerThresholdPos = (400,350)
		self._TwoPlayerThresholdValPos = (400, 375)
		self._1pUpArrowPos = (200, 389)
		self._1pDownArrowPos = (200, 412)
		self._2pUpArrowPos = (500, 389)
		self._2pDownArrowPos = (500, 412)
		self._SoundPos = (700, 350)
		self._TutorialPos = (100, 200)
		self._UnselectedColor = (0,0,0)
		self._SelectedColor = (255, 0, 0)
		self._Title = self._TitleFont.render('Shaky Table',True,self._UnselectedColor)
		self._OnePlayer = self._PlayerFont.render('One Player',True,self._UnselectedColor)
		self._TwoPlayer = self._PlayerFont.render('Two Player',True,self._UnselectedColor)
		self._OnePlayerThresholdTitle = self._SmallerFont.render('Player 1 Threshold',True,self._UnselectedColor)
		self._TwoPlayerThresholdTitle = self._SmallerFont.render('Player 2 Threshold',True,self._UnselectedColor)
		self._OnePlayerThreshold = self._LargerFont.render('70',True,self._UnselectedColor)
		self._TwoPlayerThreshold = self._LargerFont.render('70',True,self._UnselectedColor)
		# self._Tutorial = self._TutorialFont.render('How to Play',True,self._UnselectedColor)
		self.P1Up = Triange((16,14), self._1pUpArrowPos)
		self.P1Down = Triange((16,14), self._1pDownArrowPos, flipped=True)
		self.P2Up = Triange((16,14), self._2pUpArrowPos)
		self.P2Down = Triange((16,14), self._2pDownArrowPos, flipped=True)
		self.hover1P = False
		self.hover2P = False
		# self.hoverTutorial = False
		self.P1Threshold = 70
		self.P2Threshold = 70
		
	def draw(self):
		#print self._screen.get_size()
		self.titleParticles.move()
		self.titleParticles.draw()
		self.P1Up.draw(self._screen)
		self.P1Down.draw(self._screen)
		self.P2Up.draw(self._screen)
		self.P2Down.draw(self._screen)
		self._screen.blit(self._Title, self._TitlePos)
		self._screen.blit(self._OnePlayer, self._OnePlayerPos)
		self._screen.blit(self._TwoPlayer, self._TwoPlayerPos)
		self._screen.blit(self._OnePlayerThresholdTitle, self._OnePlayerThresholdPos)
		self._screen.blit(self._TwoPlayerThresholdTitle, self._TwoPlayerThresholdPos)
		self._screen.blit(self._OnePlayerThreshold, self._OnePlayerThresholdValPos)
		self._screen.blit(self._TwoPlayerThreshold, self._TwoPlayerThresholdValPos)
		# self._screen.blit(self._Tutorial, self._TutorialPos)
		
		
	def OnePHover(self):
		self._OnePlayer = self._PlayerFont.render('One Player',True,self._SelectedColor)
		self.hover1P = True
	
	def OnePLeave(self):
		self._OnePlayer = self._PlayerFont.render('One Player',True,self._UnselectedColor)
		self.hover1P = False
		
	def TwoPHover(self):
		self._TwoPlayer = self._PlayerFont.render('Two Player',True,self._SelectedColor)
		self.hover2P = True
	
	def TwoPLeave(self):
		self._TwoPlayer = self._PlayerFont.render('Two Player',True,self._UnselectedColor)
		self.hover2P = False

	# def TutorialHover(self):
	# 	self._Tutorial = self._TutorialFont.render('How to Play',True,self._SelectedColor)
	# 	self.hoverTutorial = True

	# def TutorialLeave(self):
	# 	self._Tutorial = self._TutorialFont.render('How to Play',True,self._UnselectedColor)
	# 	self.hoverTutorial = False

	# def ToggleMute(self, status):
	# 	if (status):
	# 		self.SoundIcon = pygame.transform.smoothscale(pygame.image.load(os.path.join(_mainDir, _MuteImage)), _MuteSize)
	# 		return False
	# 	else:
	# 		self.SoundIcon = pygame.transform.smoothscale(pygame.image.load(os.path.join(_mainDir, _SoundImage)), _SoundSize)
	# 		return True

	def IncrementThreshold(self, player, incVal = 1):
		if player == 1:
			self.P1Threshold += incVal
			self._OnePlayerThreshold = self._LargerFont.render(str(self.P1Threshold),True,self._UnselectedColor)
		if player == 2:
			self.P2Threshold += incVal
			self._TwoPlayerThreshold = self._LargerFont.render(str(self.P2Threshold),True,self._UnselectedColor)

class Particles:

	def __init__ (self, containers, screen, center):
		self._particles = []
		self._containers = containers
		self._screen = screen
		self._center = center
	
	def addParticle(self):
		self._particles.append(Particle(self._center.copy(), self._containers, self._screen))
	
	def move(self):
		if (len(self._particles) < maxParticles):
			self.addParticle()
		for particle in self._particles:
			if particle.alpha <= 0:
				self._particles.remove(particle)
			else:
				particle.move()
	
	def draw (self):
		for particle in self._particles:
			particle.draw()

class Particle (Sprite.Sprite):

	def __init__ (self, loc, containers, screen, alpha=1.):
		v0 = numpy.array([random.uniform(-0.25,0.25), random.uniform(-0.25,0.25)])
		v1 = v0 * particleSpeed
		Sprite.Sprite.__init__(self, containers, screen, imageFile='star.jpg', size=(20,20), x=loc, v=v1)
		self.alpha = alpha
		self._surface.set_colorkey((255,255,255))
		self.kill()	# particle don't get to be in any group
	
	def move (self):
		Sprite.Sprite.move(self)
		self._surface.set_alpha(255.*self.alpha)
		self.alpha -= alphaDecay

class Triange (pygame.Surface):

	def __init__ (self, size=(30,30), location=(0,0), flipped=False):
		super(Triange, self).__init__(size)
		self.size = size
		self.fill((255,255,255,255))
		self.location = location
		self.flipped = flipped
		self.selected = False
		pygame.draw.polygon(self, black, self._getCoordinates(), 2)
	
	def draw (self, screen):
		screen.blit(self, self.location)

	def highlight (self):
		pygame.draw.polygon(self, red, self._getCoordinates(), 2)
		self.selected = True
	
	def unhighlight (self):
		pygame.draw.polygon(self, black, self._getCoordinates(), 2)
		self.selected = False

	def _getCoordinates (self):
		size = self.size
		if not self.flipped:
			return [((size[0]-2)/2,0),(0,size[1]-2),(size[0]-2,size[1]-2)]
		else:
			return [((size[0]-2)/2,size[1]),(0,0),(size[0]-2,0)]
		