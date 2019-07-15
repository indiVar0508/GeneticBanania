import pygame
from Brain import mutableBrain
import numpy as np

class GeneralPlayer():

	def __init__(self, gameDisplay, gameWidth = 600, gameHeight = 400):
		self.gameWidth = gameWidth
		self.gameHeight = gameHeight
		self.gameDisplay = gameDisplay
		self.imgItr = 1
		self.x, self.y = 50, self.gameHeight // 2
		self.width, self.height = 30, 35
		self.step = 5
		self.characterDefault = pygame.image.load(r'Resources\Character\StandBy\{}.png'.format(self.imgItr))
		self.left = self.right = self.up = self.down = False
		self.visionLimit = 50
		self.leftVision = self.rightVision = self.upVision = self.downVision = (255, 255 ,255)
		self.leftVisionBlock = (self.x + self.width // 2 - self.visionLimit, self.y + self.height // 2)
		self.rightVisionBlock = (self.x + self.width // 2 + self.visionLimit, self.y + self.height // 2)
		self.upVisionBlock = (self.x + self.width // 2, self.y + self.height // 2 - self.visionLimit)
		self.downVisionBlock = (self.x + self.width // 2, self.y + self.height // 2 + self.visionLimit)
		self.leftDistance = self.rightDistace = self.upDistance = self.downDistance = self.visionLimit
		self.fitness = 0.0 #score

	def takeStep(self, dir_):
		self.steps -= 1
		if dir_ == 'Left':
			self.x -= self.step
			if self.x < 0: 
				self.x = 0
				self.left = False
				self.fitness -= 0.0001
				# self.leftVisionBlock = (self.leftVisionBlock[0] + self.step, self.leftVisionBlock[1]) # i was lazy enough to change it every where to list :P
		if dir_ == 'Right':
			self.x += self.step
			if self.x + self.width > self.gameWidth: 
				self.x = self.gameWidth - self.width
				self.right = False
				self.fitness -= 0.0001
				# self.rightVisionBlock = (self.rightVisionBlock[0] - self.step, self.rightVisionBlock[1])
		if dir_ == 'Up':
			self.y -= self.step
			if self.y < 0: 
				self.y = 0
				self.up = False
				self.fitness -= 0.0001
				# self.upVisionBlock = (self.upVisionBlock[0], self.upVisionBlock[1] + self.step)
		if dir_ == 'Down':
			self.y += self.step
			if self.y + self.height > self.gameHeight: 
				self.y = self.gameHeight - self.height
				self.down = False
				self.fitness -= 0.0001
				# self.downVisionBlock = (self.downVisionBlock[0], self.downVisionBlock[1] - self.step)
		self.handleVision()

	
	def decideMovement(self, cords):
		if self.up: yield self.showMovement('Up', cords)
		elif self.down: yield self.showMovement('Down', cords)
		elif self.left: yield self.showMovement('Left', cords)
		elif self.right: yield self.showMovement('Right', cords)
		# else: print('yoyo')



	def hurdleContact(self, cords):
		self.handleHurdleVision(cords)
		condn, cords = self.contactingHurdle(cords)
		if condn:
			self.fitness -= 0.000025
			if self.left: 
				self.x = cords[0] + cords[2] + 6
				self.left = False
				self.upVisionBlock = (self.upVisionBlock[0] + self.step, self.upVisionBlock[1])
				self.downVisionBlock = (self.downVisionBlock[0] + self.step, self.downVisionBlock[1])
			elif self.right: 
				self.x = cords[0] - self.width - 6
				self.right = False
				self.upVisionBlock = (self.upVisionBlock[0] - self.step, self.upVisionBlock[1])
				self.downVisionBlock = (self.downVisionBlock[0] - self.step, self.downVisionBlock[1])
			elif self.up: 
				self.y = cords[1] + cords[3] + 6
				self.up = False
				self.leftVisionBlock = (self.leftVisionBlock[0], self.leftVisionBlock[1] + self.step)
				self.rightVisionBlock = (self.rightVisionBlock[0], self.rightVisionBlock[1] + self.step)
			elif self.down: 
				self.y = cords[1] - self.height	- 6
				self.down = False
				self.leftVisionBlock = (self.leftVisionBlock[0], self.leftVisionBlock[1] - self.step)
				self.rightVisionBlock = (self.rightVisionBlock[0], self.rightVisionBlock[1] - self.step)
		# 	return True
		# return False

	def contactingHurdle(self, cordinates):
		for cords in cordinates:
			if (cords[0] < self.x + 5 < cords[0] + cords[2] or cords[0] < self.x + self.width - 5 < cords[0] + cords[2]) and\
			(cords[1] < self.y + 5 < cords[1] + cords[3] or cords[1] < self.y + self.height - 5 < cords[1] + cords[3]): return True, cords
		return False, None


	def handleHurdleVision(self, cordinates):
		# self.leftVision = self.rightVision = self.upVision = self.downVision = (255, 255 ,255)
		for idx, cords in enumerate(cordinates):
			if self.x + self.width // 2 >= cords[0] + cords[2]  and cords[1] <= self.y + self.height // 2 <= cords[1] + cords[3] and self.x + self.width // 2 - (cords[0] + cords[2]) <= self.visionLimit:
				self.leftDistance = self.x + self.width // 2 - (cords[0] + cords[2])
				self.leftVisionBlock = (cords[0] + cords[2], self.y + self.height // 2)
				self.leftVision = (255, 0 , 0)
			elif self.x + self.width // 2 <= cords[0] and cords[1] <= self.y + self.height // 2 <= cords[1] + cords[3] and cords[0] - (self.x + self.width // 2) <= self.visionLimit:
				self.rightDistace =  cords[0] - (self.x + self.width // 2)
				self.rightVisionBlock = (cords[0], self.y + self.height // 2)
				self.rightVision = (255, 0 , 0)
			elif self.y + self.height // 2 >= cords[1] + cords[3] and cords[0] <= self.x + self.width // 2 <= cords[0] + cords[2] and self.y + self.height // 2 - (cords[1] + cords[3]) <= self.visionLimit:
				self.upDistance =  self.y + self.height // 2 - (cords[1] + cords[3])
				self.upVisionBlock = (self.x + self.width // 2, cords[1] + cords[3])
				self.upVision = (255, 0 , 0)
			elif self.y + self.height // 2 <= cords[1] and cords[0] <= self.x + self.width // 2 <= cords[0] + cords[2] and cords[1] - (self.y + self.height // 2) <= self.visionLimit:
				self.downDistance =  cords[1] - (self.y + self.height // 2)
				self.downVisionBlock = (self.x + self.width // 2, cords[1])
				self.downVision = (255, 0 , 0)



	def showVision(self):
		pygame.draw.line(self.gameDisplay, self.leftVision, (self.x + self.width // 2, self.y + self.height // 2), self.leftVisionBlock)
		pygame.draw.line(self.gameDisplay, self.rightVision, (self.x + self.width // 2, self.y + self.height // 2), self.rightVisionBlock)
		pygame.draw.line(self.gameDisplay, self.upVision, (self.x + self.width // 2, self.y + self.height // 2), self.upVisionBlock)
		pygame.draw.line(self.gameDisplay, self.downVision, (self.x + self.width // 2, self.y + self.height // 2), self.downVisionBlock)

	def handleVision(self):
		self.leftVision = self.rightVision = self.upVision = self.downVision = (255, 255 ,255)
		if (self.x + self.width // 2) - self.visionLimit < 0: 
			self.leftVisionBlock = (0, self.y + self.height // 2)
			self.leftVision = (255, 0, 0)
			self.leftDistance = self.x + self.width // 2
		else: 
			self.leftVisionBlock = (self.x + self.width // 2 - self.visionLimit, self.y + self.height // 2)
			self.leftDistance = self.visionLimit

		if self.x + self.width // 2 + self.visionLimit > self.gameWidth: 
			self.rightVisionBlock = (self.gameWidth, self.y + self.height // 2)
			self.rightVision = (255, 0, 0)
			self.rightDistace =  self.gameWidth - (self.x + self.width // 2)
		else: 
			self.rightDistace = self.visionLimit
			self.rightVisionBlock = (self.x + self.width // 2 + self.visionLimit, self.y + self.height // 2)

		if self.y + self.height // 2 - self.visionLimit < 0: 
			self.upDistance =  self.y + self.height // 2
			self.upVisionBlock = (self.x + self.width // 2, 0)
			self.upVision = (255, 0, 0)
		else: 
			self.upDistance = self.visionLimit
			self.upVisionBlock = (self.x + self.width // 2, self.y + self.height // 2 - self.visionLimit)

		if self.y + self.height // 2 + self.visionLimit > self.gameHeight: 
			self.downDistance =   self.gameHeight - (self.y + self.height // 2)
			self.downVisionBlock = (self.x + self.width // 2, self.gameHeight)
			self.downVision = (255, 0, 0)
		else: 
			self.downDistance = self.visionLimit
			self.downVisionBlock = (self.x + self.width // 2, self.y + self.height // 2 + self.visionLimit)


	def showPlayerStandBy(self):
		self.gameDisplay.blit(self.characterDefault, (self.x, self.y))

	def showMovement(self, dir, cords):
		movDir = 'Resources\\Character\\Movements\\' + dir + 'Movement\\'
		# self.fitness += 0.5
		for i in range(1, 5):
			self.takeStep(dir)
			# if not (self.left or self.up or self.right or self.down) or self.hurdleContact(cords): return self.characterDefault
			# if self.hurdleContact(cords): return self.characterDefault
			self.hurdleContact(cords)
			if not (self.left or self.up or self.right or self.down): 
				self.steps -= 10
				# self.fitness -= 0.001
				yield (self.characterDefault, True)
			img = pygame.image.load(movDir + '{}.png'.format(i))
			yield (img, False)



class MutablePlayer(GeneralPlayer):

	def __init__(self, gameDisplay, gameWidth = 600, gameHeight = 400, layers = [4, 2, 4], learningRate = 0.09, activationFunc = 'relu', Gaussian = False, weights = None, biasses = None):
		super().__init__(gameDisplay, gameWidth = 600, gameHeight = 400)
		self.Brain = mutableBrain(layers = layers, learningRate = learningRate, activationFunc = activationFunc, Gaussian = Gaussian, weights = weights, biasses = biasses)
		self.alive = True
		self.steps = 10000

	def isAlive(self, hurdles):
		# print(self.fitness)
		if (self.steps < 0) or (self.steps < 8000 and self.x < hurdles[0][0]) \
		or (self.steps < 7000 and (hurdles[0][0] < self.x < hurdles[1][0]))\
		or (self.steps < 5000 and (hurdles[1][0] < self.x < hurdles[3][0]))\
		or (self.steps < 4000 and (hurdles[3][0] < self.x < hurdles[4][0])) \
		or (self.steps < 2000 and (hurdles[4][0] < self.x < hurdles[6][0]))\
		or (self.steps < 1000 and (hurdles[6][0] < self.x < hurdles[8][0])): 
			self.alive = False
			return False
		# if :
			self.alive = False
			return False
		return True

	def gotFood(self, foodLoc, foodSize):
		if (foodLoc[0] <= self.x <= foodLoc[0] + foodSize or foodLoc[0] <= self.x + self.width <= foodLoc[0] + foodSize) \
		and (foodLoc[1] <= self.y <= foodLoc[1] + foodSize or foodLoc[1] <= self.y + self.height <= foodLoc[1] + foodSize):
			self.alive = False
			print('Yeah.!')
			print(self.Brain.layers)
			return 100
		return 0


	def getFitness(self, foodCords, foodSize, hurdles):
		self.fitness += (1 / abs(self.x - foodCords[0]))
		i = len(hurdles) - 2
		while i >= 0 and hurdles[i][0] > self.x: i -= 1
		self.fitness += (1 / (abs(self.y - hurdles[i+1][1]) +1))
		self.fitness += (i + 1) * 10 + self.gotFood(foodCords, foodSize)
		self.fitness += (1 / (self.steps + 2))
		

	def biCrossOver(parentOne, parentTwo):
		child = MutablePlayer(gameDisplay = parentOne.gameDisplay, gameWidth = parentOne.gameWidth, gameHeight = parentOne.gameHeight, layers = parentOne.Brain.layers, \
			activationFunc = parentOne.Brain.activationFunc, Gaussian = parentTwo.Brain.Gaussian,\
			 weights = parentOne.Brain.weights, biasses = parentTwo.Brain.biasses)
		for idx, _ in enumerate(child.Brain.weights):
			for row, __ in enumerate(child.Brain.weights[idx]):
				for col, ___ in enumerate(child.Brain.weights[idx][row]):
					if np.random.random() < 0.5: child.Brain.weights[idx][row][col] = np.copy(parentOne.Brain.weights[idx][row][col])
					else: child.Brain.weights[idx][row][col] = np.copy(parentTwo.Brain.weights[idx][row][col])
		for idx, _ in enumerate(child.Brain.biasses):
			for row, __ in enumerate(child.Brain.biasses[idx]):
				for col, ___ in enumerate(child.Brain.biasses[idx][row]):
					if np.random.random() < 0.5: child.Brain.biasses[idx][row][col] = np.copy(parentOne.Brain.biasses[idx][row][col])
					else: child.Brain.biasses[idx][row][col] = np.copy(parentTwo.Brain.biasses[idx][row][col])
		return child

	def uniCrossOver(parentOne):
		child = MutablePlayer(gameDisplay = parentOne.gameDisplay, gameWidth = parentOne.gameWidth, gameHeight = parentOne.gameHeight, layers = parentOne.Brain.layers, \
			activationFunc = parentOne.Brain.activationFunc, Gaussian = parentOne.Brain.Gaussian,\
			 weights = parentOne.Brain.weights, biasses = parentOne.Brain.biasses)
		for idx, _ in enumerate(child.Brain.weights):
			child.Brain.weights[idx] = np.copy(parentOne.Brain.weights[idx])
			child.Brain.biasses[idx] = np.copy(parentOne.Brain.biasses[idx])
		return child



	def think(self, foodCords):
		foodDistance = abs(self.x - foodCords[0]) / self.gameWidth
		state = np.array([self.leftDistance / self.visionLimit, self.rightDistace / self.visionLimit, self.upDistance / self.visionLimit, self.downDistance / self.visionLimit,\
						self.left, self.right, self.up, self.down])
		action = self.Brain.predict(X = state, show = 'softmax')

		if action == 0: 
			self.up = True
			self.left = self.right = self.down = False
		elif action == 1:
			self.down = True
			self.left = self.right = self.up = False
		elif action == 2:
			self.left = True
			self.right = self.up = self.down = False
		elif action == 3:
			self.right = True
			self.left = self.up = self.down = False
