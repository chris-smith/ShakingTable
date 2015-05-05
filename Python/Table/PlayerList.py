import Player, pygame, time, datetime
from HXMReceiver import *

class PlayerList:
	
	def __init__ (self, containers, screen, players=1, thresholds=(70,70), sound_on=True):
		self._screen = screen
		self.hxm = HXMReceiver(minDevices=players)
		self.hxm.run()
		self.players = []
		self.stressedPlayers = []
		for p in range(players):
			self.players.append(Player.Player(containers, screen, self.hxm.devices[p], thresholds[p], self, sound_on))
		t = datetime.datetime.fromtimestamp(time.time())
		self.outfile = './Log/Log ' + t.strftime('%Y-%m-%d %H.%M.%S') + '.csv'
		f = open(self.outfile, 'w')
		f.write('Start time: {0}, Players: {1}\n'.format(time.time(), players))
		f.close()
	
	def __getitem__(self, key):
		return self.players[key]

	def accel(self, player, a):
		if len(self.players) > player:
			self.players[player].accel(a)
	
	def fire(self, player):
		self.players[player].fire()
	
	def move(self):
		for player in self.players:
			player.move()
			if (len(self.stressedPlayers) > 0):
				player.startCountdown()
			else:
				player.stopCountdown()
	
	def draw(self):
		for player in self.players:
			player.draw()
			
	def playerBullets(self):
		bullets = []
		for player in players:
			bullets.append(player.bullets)
		return bullets

	def tellEveryoneImStressed(self, player):
		if player not in self.stressedPlayers:
			self.stressedPlayers.append(player)

	def tellEveryoneImBetter(self, player):
		if player in self.stressedPlayers:
			self.stressedPlayers.remove(player)

	def __del__ (self):
		self.hxm.close()

	def close (self):
		f = open(self.outfile, 'a')
		f.write('End time: {0}, Score: {1}\n'.format(time.time(), self.players[0].score))
		f.write(self.hxm.log())
		f.close()
		self.__del__()

