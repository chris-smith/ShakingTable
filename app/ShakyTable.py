# This file is the same table_interface_v1.py

import serial, pygame, sys, time, os, random, re, logging, io
from datetime import datetime
from pygame.locals import *
import threading
import Table.Background, Table.IntroScreen, Table.GameScreen #Table.PlayerList, Table.Player, 

WIDTH = 650
HEIGHT = 550 #300
SCREENRECT     = Rect(0, 0, WIDTH, HEIGHT)

MAX_POWER = 120
MID_POWER = 80

serRead = [serial.Serial('/dev/tty.usbmodem1d1111', 9600), serial.Serial('/dev/tty.usbmodem1d1121', 9600)]
serWrite = serial.Serial('/dev/tty.usbmodem1421', 9600)
thresholds = [70, 70]
heartRates = [0, 0]
tableRunning = False

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)
lock = threading.Lock()

# dummy variables
# serRead = ['/dev/tty.usbmodem1d1111','/dev/tty.usbmodem1d1121']
# serWrite = '/dev/tty.usbmodem1421'

def introInput(events):
	for event in events: 
		#print event
		if event.type == MOUSEMOTION:
			mousepos = pygame.mouse.get_pos()
			return {'MOUSEMOVE': mousepos}
		if event.type == MOUSEBUTTONDOWN:
			if (pygame.mouse.get_pressed()[0] == 1):
				return {'MOUSEPRESS': pygame.mouse.get_pressed()[0]}
		if event.type == QUIT: 
			sys.exit(0)
	return False

def introLoop():
	screen = pygame.display.get_surface()
	background = Table.Background.Background(screen)
	introScreen = Table.IntroScreen.IntroScreen(screen)
	while True:
		action = introInput(pygame.event.get())
		if (action):
			if ('MOUSEMOVE' in action):
				r1 = introScreen._OnePlayer.get_rect()
				if detectHit(introScreen._OnePlayerPos, r1.bottomright, action['MOUSEMOVE'], (0,0)):
					introScreen.OnePHover()
				else:
					if (introScreen.hover1P):
						introScreen.OnePLeave()
				r2 = introScreen._TwoPlayer.get_rect()
				if detectHit(introScreen._TwoPlayerPos, r2.bottomright, action['MOUSEMOVE'], (0,0)):
					introScreen.TwoPHover()
				else:
					if (introScreen.hover2P):
						introScreen.TwoPLeave()
				r = introScreen.P1Up.get_rect()
				if detectHit(introScreen._1pUpArrowPos, r.bottomright, action['MOUSEMOVE'], (0,0)):
					introScreen.P1Up.highlight()
				else:
					introScreen.P1Up.unhighlight()
				r = introScreen.P1Down.get_rect()
				if detectHit(introScreen._1pDownArrowPos, r.bottomright, action['MOUSEMOVE'], (0,0)):
					introScreen.P1Down.highlight()
				else:
					introScreen.P1Down.unhighlight()
				r = introScreen.P2Up.get_rect()
				if detectHit(introScreen._2pUpArrowPos, r.bottomright, action['MOUSEMOVE'], (0,0)):
					introScreen.P2Up.highlight()
				else:
					introScreen.P2Up.unhighlight()
				r = introScreen.P2Down.get_rect()
				if detectHit(introScreen._2pDownArrowPos, r.bottomright, action['MOUSEMOVE'], (0,0)):
					introScreen.P2Down.highlight()
				else:
					introScreen.P2Down.unhighlight()
				# r = introScreen._Tutorial.get_rect()
				# if detectHit(introScreen._TutorialPos, r.bottomright, action['MOUSEMOVE'], (0,0)):
				# 	introScreen.TutorialHover()
				# else:
				# 	if introScreen.hoverTutorial:
				# 		introScreen.TutorialLeave()
			if ('MOUSEPRESS' in action):
				if introScreen.hover1P:
					thresholds = [introScreen.P1Threshold, introScreen.P2Threshold]
					return 1
				if introScreen.hover2P:
					thresholds = [introScreen.P1Threshold, introScreen.P2Threshold]
					return 2
				if introScreen.P1Up.selected:
					introScreen.IncrementThreshold(player=1)
				if introScreen.P1Down.selected:
					introScreen.IncrementThreshold(player=1,incVal=-1)
				if introScreen.P2Up.selected:
					introScreen.IncrementThreshold(player=2)
				if introScreen.P2Down.selected:
					introScreen.IncrementThreshold(player=2,incVal=-1)
				# if introScreen.hoverTutorial:
				# 	tutorialLoop()
		
				#print items_hit
		background.draw()
		introScreen.draw()
		pygame.display.flip()

def gameLoop(players=2):
	print "gameLoop"
	global tableRunning 
	tableRunning = True
	# gameThread = threading.Thread(name="gameThread", target=pygameLoop, args=(players,))
	serialThread = threading.Thread(name="serialThread", target=serialLoop)
	# pygameLoop(players,thresholds)
	# gameThread.start()
	serialThread.start()
	status = pygameLoop(players)

	# gameThread.join()
	serialThread.join()

	return status

def serialLoop():
	logging.debug('Starting, thresholds = ' + str(thresholds))
	dummy_rate = [50,50]
	motorPower = [0, 0]
	while tableRunning:
		# lock.acquire()
		for s in serRead:			
			index = serRead.index(s)
			raw = s.readline()
			# raw = str(dummy_rate[index])
			dummy_rate[index] = dummy_rate[index] + 1
			heartRates[index] = int(filter(lambda x: x.isdigit(), raw))
			if heartRates[index] > thresholds[index]:
				motorPower[index] = MAX_POWER
			elif heartRates[index] > thresholds[index] - 5:
				motorPower[index] = MID_POWER
			else:
				motorPower[index] = 0
			print "{0},{1},{2},{3}".format(index, datetime.now(), heartRates[index], motorPower[index])
			# time.sleep(0.5)
		serWrite.write(chr(max(motorPower)))
	logging.debug('Leaving')

def pygameLoop(players):
	global thresholds, tableRunning	
	logging.debug('Starting, thresholds = ' + str(thresholds))
	screen  = pygame.display.get_surface()
	background = Table.Background.Background(screen)
	gameScreen = Table.GameScreen.GameScreen(screen, players, thresholds)

	while True:
		lock.acquire()
		action = introInput(pygame.event.get())
		if (action):
			if ('MOUSEMOVE' in action):
				r = gameScreen.P1Up.get_rect()
				if detectHit(gameScreen._1pUpArrowPos, r.bottomright, action['MOUSEMOVE'], (0,0)):
					gameScreen.P1Up.highlight()
				else:
					gameScreen.P1Up.unhighlight()
				r = gameScreen.P1Down.get_rect()
				if detectHit(gameScreen._1pDownArrowPos, r.bottomright, action['MOUSEMOVE'], (0,0)):
					gameScreen.P1Down.highlight()
				else:
					gameScreen.P1Down.unhighlight()
				r = gameScreen.P2Up.get_rect()
				if detectHit(gameScreen._2pUpArrowPos, r.bottomright, action['MOUSEMOVE'], (0,0)):
					gameScreen.P2Up.highlight()
				else:
					gameScreen.P2Up.unhighlight()
				r = gameScreen.P2Down.get_rect()
				if detectHit(gameScreen._2pDownArrowPos, r.bottomright, action['MOUSEMOVE'], (0,0)):
					gameScreen.P2Down.highlight()
				else:
					gameScreen.P2Down.unhighlight()
				r = gameScreen._QuitButton.get_rect()
				if detectHit(gameScreen._QuitButtonPos, r.bottomright, action['MOUSEMOVE'], (0,0)):
					gameScreen.QuitButtonHover()
				else:
					gameScreen.QuitButtonLeave()
			if ('MOUSEPRESS' in action):
				if gameScreen.P1Up.selected:
					gameScreen.IncrementThreshold(player=1)
				if gameScreen.P1Down.selected:
					gameScreen.IncrementThreshold(player=1,incVal=-1)
				if gameScreen.P2Up.selected:
					gameScreen.IncrementThreshold(player=2)
				if gameScreen.P2Down.selected:
					gameScreen.IncrementThreshold(player=2,incVal=-1)
				if gameScreen.hoverQuitButton:
					tableRunning = False
					return False
		background.draw()
		gameScreen.draw(heartRates)
		pygame.display.flip()
		lock.release()

def detectHit(box1Pos, box1Size, box2Pos, box2Size):
	if ((box1Pos[0] <= box2Pos[0] + box2Size[0]) and 
		(box1Pos[0] + box1Size[0] >= box2Pos[0]) and
		(box1Pos[1] <= box2Pos[1] + box2Size[1]) and
		(box1Pos[1] + box1Size[1] >= box2Pos[1])):
		return True
	return False

def runGame():
	players = introLoop()
	return gameLoop(players)

if __name__ == '__main__':
	pygame.init()
	window = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Shaky Table')
	screen = pygame.display.get_surface()
	status = runGame()
	while(status == True):
		status = runGame()