import operator
import random

class Species:
    def __init__(self, player):
        self.players = []
        self.averageFitness = 0
        self.threshold = 1.2
        self.players.append(player)
        self.benchmarkFitness = player.fitness
        self.benchmarkBrain = player.brain.clone()
        self.champion = player.clone()
        self.staleness = 0

    def similarity(self, brain):
        similarity = self.weightDifference(self.benchmarkBrain, brain)
        return self.threshold > similarity
    
    @staticmethod
    def weightDifference(brain1, brain2):
        totalWeightDifference = 0
        for i in range(0, len(brain1.connections)):
            for j in range(0, len(brain2.connections)):
                if i == j:
                    totalWeightDifference += abs(brain1.connections[i].weight - 
                                                 brain2.connections[j].weight)
                    
        return totalWeightDifference
    
    def addToSpecies(self, player):
        self.players.append(player)

    def sortPlayersByFitness(self):
        self.players.sort(key = operator.attrgetter("fitness"), reverse=True)
        if self.players[0].fitness > self.benchmarkFitness:
            self.staleness = 0
            self.benchmarkFitness = self.players[0].fitness
            self.champion = self.players[0].clone()
        else:
            self.staleness += 1

    def calculateAverageFitness(self):
        totalFitness = 0
        for p in self.players:
            totalFitness += p.fitness
        if self.players:
            self.averageFitness = int(totalFitness / len(self.players))
        else:
            self.averageFitness = 0

    def offspring(self):
        baby = self.players[random.randint(1, len(self.players)) - 1].clone()
        baby.brain.mutate()
        return baby