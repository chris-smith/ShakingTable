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

class GameScreen:

	def __init__(self, screen, players=2, thresholds=[70,70]):
		all = pygame.sprite.RenderUpdates()
		self._screen = screen
		self._players = players
		# self.title = Sprite.Sprite(all, screen, imageFile='rage_title.png', size=(424,57), x=numpy.array([100.,100.]))
		# self.titleParticles = Particles(all, screen, numpy.array([100.,100.]))
		self._PlayerFont = pygame.font.SysFont('Helvetica', 30, bold=True)
		self._TutorialFont = pygame.font.SysFont('Helvetica', 42, bold=True)
		self._SmallerFont = pygame.font.SysFont('Baskerville', 16, bold=False, italic=True)
		self._LargerFont = pygame.font.SysFont('Helvetica', 60, bold=True)
		self._TitleFont = pygame.font.SysFont('comicsansms',70,bold=True)
		self._QuitButtonFont = pygame.font.SysFont('comicsansms', 30, bold=False)
		self._TitlePos = (40,50)
		self._OnePlayerPos = (100,200)
		self._OnePlayerRatePos = (100,250)
		self._OnePlayerRateValPos = (100, 275)
		self._OnePlayerThresholdPos = (100,375)
		self._OnePlayerThresholdValPos = (100,400)
		self._TwoPlayerPos = (400,200)
		self._TwoPlayerRatePos = (400,250)
		self._TwoPlayerRateValPos = (400,275)
		self._TwoPlayerThresholdPos = (400,375)
		self._TwoPlayerThresholdValPos = (400,400)
		self._1pUpArrowPos = (200, 414)
		self._1pDownArrowPos = (200, 437)
		self._2pUpArrowPos = (500, 414)
		self._2pDownArrowPos = (500, 437)
		self._QuitButtonPos = (275,500)
		self._UnselectedColor = (0,0,0)
		self._SelectedColor = (255, 0, 0)
		self._Title = self._TitleFont.render('Game in Progress',True,self._UnselectedColor)
		self._OnePlayer = self._PlayerFont.render('Player One',True,self._UnselectedColor)
		self._TwoPlayer = self._PlayerFont.render('Player Two',True,self._UnselectedColor)
		self._OnePlayerRateTitle = self._SmallerFont.render('Player 1 Rate',True,self._UnselectedColor)
		self._TwoPlayerRateTitle = self._SmallerFont.render('Player 2 Rate',True,self._UnselectedColor)
		self._OnePlayerRate = self._LargerFont.render('0',True,self._UnselectedColor)
		self._TwoPlayerRate = self._LargerFont.render('0',True,self._UnselectedColor)
		self._OnePlayerThresholdTitle = self._SmallerFont.render('Player 1 Threshold',True,self._UnselectedColor)
		self._TwoPlayerThresholdTitle = self._SmallerFont.render('Player 2 Threshold',True,self._UnselectedColor)
		self._OnePlayerThreshold = self._LargerFont.render(str(thresholds[0]),True,self._UnselectedColor)
		self._TwoPlayerThreshold = self._LargerFont.render(str(thresholds[1]),True,self._UnselectedColor)
		self._QuitButton = self._QuitButtonFont.render('Quit', True, self._UnselectedColor)
		# self._Tutorial = self._TutorialFont.render('How to Play',True,self._UnselectedColor)
		self.P1Up = Triange((16,14), self._1pUpArrowPos)
		self.P1Down = Triange((16,14), self._1pDownArrowPos, flipped=True)
		self.P2Up = Triange((16,14), self._2pUpArrowPos)
		self.P2Down = Triange((16,14), self._2pDownArrowPos, flipped=True)
		self.hoverQuitButton = False
		# self.hover1P = False
		# self.hover2P = False
		self.P1Threshold = thresholds[0]
		self.P2Threshold = thresholds[1]
		
	def draw(self, rates=[0,0]):
		self._OnePlayerRate = self._LargerFont.render(str(rates[0]),True,self._UnselectedColor)
		self.P1Up.draw(self._screen)
		self.P1Down.draw(self._screen)
		self._screen.blit(self._Title, self._TitlePos)
		self._screen.blit(self._OnePlayer, self._OnePlayerPos)
		self._screen.blit(self._OnePlayerRateTitle, self._OnePlayerRatePos)
		self._screen.blit(self._OnePlayerRate, self._OnePlayerRateValPos)
		self._screen.blit(self._OnePlayerThresholdTitle, self._OnePlayerThresholdPos)
		self._screen.blit(self._OnePlayerThreshold, self._OnePlayerThresholdValPos)
		self._screen.blit(self._QuitButton, self._QuitButtonPos)
		if self._players == 2:
			self._TwoPlayerRate = self._LargerFont.render(str(rates[1]),True,self._UnselectedColor)
			self.P2Up.draw(self._screen)
			self.P2Down.draw(self._screen)
			self._screen.blit(self._TwoPlayer, self._TwoPlayerPos)
			self._screen.blit(self._TwoPlayerRateTitle, self._TwoPlayerRatePos)	
			self._screen.blit(self._TwoPlayerRate, self._TwoPlayerRateValPos)
			self._screen.blit(self._TwoPlayerThresholdTitle, self._TwoPlayerThresholdPos)
			self._screen.blit(self._TwoPlayerThreshold, self._TwoPlayerThresholdValPos)

	def QuitButtonHover(self):
		self._QuitButton = self._QuitButtonFont.render('Quit',True,self._SelectedColor)
		self.hoverQuitButton = True

	def QuitButtonLeave(self):
		self._QuitButton = self._QuitButtonFont.render('Quit',True,self._UnselectedColor)
		self.hoverQuitButton = False

	def IncrementThreshold(self, player, incVal = 1):
		if player == 1:
			self.P1Threshold += incVal
			self._OnePlayerThreshold = self._LargerFont.render(str(self.P1Threshold),True,self._UnselectedColor)
		if player == 2:
			self.P2Threshold += incVal
			self._TwoPlayerThreshold = self._LargerFont.render(str(self.P2Threshold),True,self._UnselectedColor)
		return [self.P1Threshold, self.P2Threshold]

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
		