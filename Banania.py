import pygame
import numpy as np
# from Agent import MutablePlayer
from Population import Population

pygame.display.set_caption('Banania')
pygame.init()

class Environment():

	def __init__(self, gameWidth = 600, gameHeight = 400):
		self.gameHeight = gameHeight
		self.gameWidth = gameWidth
		self.gameDisplay = pygame.display.set_mode((gameWidth, gameHeight))
		self.backGroundColor = (150, 0, 0)
		self.hurdleCords = []
		self.hurdleColor = (0, 255, 0)
		relDist, increment = 0.2, 0.25
		for _ in range(3):
			self.hurdleCords.append((int(relDist* self.gameWidth), int(0.1 * self.gameHeight), 20, 320))
			self.hurdleCords.append((int((relDist + 0.1) * self.gameWidth), 0, 20, 175))
			self.hurdleCords.append((int((relDist + 0.1) * self.gameWidth), 225, 20, 175))
			relDist += increment
		self.foodLoc = (int(0.9 * self.gameWidth), self.gameHeight // 2 - 25)
		self.foodSize = 30
		self.food = pygame.image.load(r'Resources\Food\banana.png')
		self.population = Population(gameDisplay = self.gameDisplay, gameWidth = gameWidth, gameHeight = gameHeight, \
			layers = [[8, 10, 4],[8, 10, 10, 10, 10, 10, 10,4],[8, 6, 4],[8, 10, 10, 4],[8, 20, 24, 4],[8, 55, 4], [8, 35, 4], [8, 35, 24, 4], [8, 24, 24, 4], [8, 7, 4], [8, 8, 5, 4],[8, 24, 15, 4], [8, 24, 4]] ,\
		 mutation = 0.1, populationSize = 100)
		# self.player = MutablePlayer(gameDisplay = self.gameDisplay, gameWidth = 600, gameHeight = 400, layers = [8, 7, 4], learningRate = 0.05, activationFunc = 'relu', Gaussian = False,\
									 # weights = None, biasses = None)

	def makeObjMsg(self, msg, fontDefination, color = (0, 0, 0)):
		msgObj = fontDefination.render(msg, True, color)
		return msgObj, msgObj.get_rect()

	def message(self, msg, color = (0, 0, 0), fontType = 'freesansbold.ttf', fontSize = 15, xpos = 10, ypos = 10):
		fontDefination = pygame.font.Font(fontType, fontSize)
		msgSurface, msgRectangle = self.makeObjMsg(msg, fontDefination, color)
		msgRectangle = (xpos, ypos)
		self.gameDisplay.blit(msgSurface, msgRectangle)

	def makeGrids(self):
		for x in range(0,self.gameWidth, 5): pygame.draw.line(self.gameDisplay, (10, 10, 10), (x, 0), (x, self.gameHeight))
		for y in range(0, self.gameHeight, 5): pygame.draw.line(self.gameDisplay, (10, 10, 10), (0, y), (self.gameWidth, y))

	def makeHurdles(self):
		for cords in self.hurdleCords: pygame.draw.rect(self.gameDisplay, self.hurdleColor, cords)

	def pauseGame(self):
		
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_s:
						return


			self.gameDisplay.fill((200, 200, 200))
			self.message(msg = "Paused.! Press S to continue...", fontSize = 30,\
				xpos = self.gameWidth // 2 - 200, ypos = self.gameHeight // 2)
			pygame.display.update()

	def defaultDisplays(self):
		self.gameDisplay.fill(self.backGroundColor)
		self.makeGrids()
		self.gameDisplay.blit(self.food, self.foodLoc)
		self.makeHurdles()


	def gotFood(self):
		if (self.foodLoc[0] <= self.player.x <= self.foodLoc[0] + self.foodSize or self.foodLoc[0] <= self.player.x + self.player.width <= self.foodLoc[0] + self.foodSize) \
		and (self.foodLoc[1] <= self.player.y <= self.foodLoc[1] + self.foodSize or self.foodLoc[1] <= self.player.y + self.player.height <= self.foodLoc[1] + self.foodSize):
			return True
		return False

	def showGame(self):
		# print(self.population.allDead())
		while not self.population.allDead(): ######
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return

			self.population.think(self.foodLoc)
			self.defaultDisplays()
			self.population.show(self.foodLoc, self.foodSize, self.hurdleCords)
			# if self.population.allDead(): print('done')
			self.message(msg = 'Generation : {} Alive : {}'.format(self.population.generation, self.population.alivePopulation), color = (250, 250, 250))
			pygame.display.update()
			# if self.population.allDead(): print('aakhri')
			# pygame.time.wait(240)
		# print('evolving', self.population.alivePopulation)
		self.population.evolve()
		# print('evolved')
	

	def run(self):

		self.pauseGame()
		while True: self.showGame()
		pygame.quit()


if __name__ == '__main__':
	env = Environment()
	env.run()