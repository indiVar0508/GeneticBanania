from Agent import MutablePlayer
import numpy as np

class Population:

	def __init__(self, gameDisplay, gameWidth = 600, gameHeight = 400, layers = [2, 2, 1] ,mutation = 0.1, populationSize = 50):
		self.populationSize = populationSize
		self.gameDisplay = gameDisplay
		self.gameWidth = gameWidth
		self.gameHeight = gameHeight
		self.mutation = mutation
		self.activationfuncsList = ['relu', 'sigmoid']
		self.Gaussian = [True, False]
		self.layers = layers
		self.players = [MutablePlayer(gameDisplay = gameDisplay, gameWidth = gameWidth, gameHeight = gameHeight, layers = self.layers[np.random.randint(len(self.layers))], \
			activationFunc = self.activationfuncsList[np.random.randint(len(self.activationfuncsList))], Gaussian = self.Gaussian[np.random.randint(len(self.Gaussian))], weights = None, biasses = None)\
			for _ in range(populationSize)]
		self.generation = 0
		self.matingPool = []
		self.bestFitness = 0
		self.bestPlayer = None
		self.total = 0.0
		self.alivePopulation = self.populationSize

	def allDead(self):
		for player in self.players:
			if player.alive: return False
		# print('all dead')
		return True

	def think(self, foodcords):
		for player in self.players:
			if player.alive: player.think(foodcords)


	def show(self, foodCords, foodSize, hurdleCords):
		# print(self.alivePopulation)
		for player in self.players:
			if player.alive:
				player.getFitness(foodCords, foodSize, hurdleCords)
				# print(self.alivePopulation)
				# player.fitness += 0.00005
				images = player.decideMovement(hurdleCords)
				for img in images: 
					for i in img: 
						# print(i)
						self.gameDisplay.blit(i[0], (player.x, player.y))
						player.showVision()
						if i[1]: break
				if not player.isAlive(hurdleCords): self.alivePopulation -= 1

				


	# def checkAlivePopulation(self):
	# 	# print(self.alivePopulation)
	# 	# print(self.players[0].fitness, self.players[0].steps)
	# 	for player in self.players:
	# 		if not player.alive: self.alivePopulation -= 1
	# 	if self.alivePopulation <= 0: return False
	# 	return True

	def evolve(self):
		self.computeFitness()
		self.naturalSelection()
		self.generate()
		self.alivePopulation = self.populationSize
		self.total = 0.0

	def computeFitness(self):
		self.bestFitness = 0
		for player in self.players: 
			fitn = player.fitness
			self.total += fitn
			if fitn > self.bestFitness: 
				self.bestFitness = fitn
				self.bestPlayer = player

	def naturalSelection(self):
		self.matingPool = []
		for player in self.players:
			score = np.ceil((player.fitness / (self.bestFitness + 1)) * 100)
			# print(score, player.fitness)
			while score > 0:
				self.matingPool.append(player)
				score -= 1
		
	def generate(self):
		self.players = []
		for _ in range(self.populationSize):
			p1 = self.matingPool[np.random.randint(0, len(self.matingPool))]
			p2 = self.matingPool[np.random.randint(0, len(self.matingPool))]
			if p1.Brain.layers != p2.Brain.layers: 
				if p1.fitness > p2.fitness: child = p1.uniCrossOver()
				else: child = p2.uniCrossOver()
			else: child = p1.biCrossOver(p2)
			child.Brain.mutate(mutationRate = self.mutation)
			self.players.append(child)