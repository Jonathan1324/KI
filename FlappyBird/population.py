import config
import player
import math
import species
import operator

class Population:
    def __init__(self, size):
        self.players = []
        self.generation = 1
        self.species = []
        self.size = size
        self.playersAlive = size
        for i in range(0, self.size):
            self.players.append(player.Player())
    
    def updateLivePlayers(self):
        for p in self.players:
            if p.alive:
                p.look()
                p.think()
                p.draw(config.WINDOW)
                p.update(config.ground)

    def killAll(self):
        for p in self.players:
            p.alive = False

    def naturalSelection(self):
        self.speciate()

        self.calculateFitness()

        self.killExtinctSpecies()

        self.killStaleSpecies()

        self.sortSpeciesByFitness

        self.nextGen()

    def speciate(self):
        for s in self.species:
            s.players = []

        for p in self.players:
            addToSpecies = False
            for s in self.species:
                if s.similarity(p.brain):
                    s.addToSpecies(p)
                    addToSpecies = True
                    break
            if not addToSpecies:
                self.species.append(species.Species(p))

    def calculateFitness(self):
        for p in self.players:
            p.calculateFitness()
        for s in self.species:
            s.calculateAverageFitness()

    def killExtinctSpecies(self):
        speciesBin = []
        for s in self.species:
            if len(s.players) == 0:
                speciesBin.append(s)

        for s in speciesBin:
            self.species.remove(s)

    def killStaleSpecies(self):
        playerBin = []
        speciesBin = []
        for s in self.species:
            if s.staleness >= 8:
                if len(self.species) > len(speciesBin) + 1:
                    speciesBin.append(s)
                    for p in s.players:
                        playerBin.append(p)
                else:
                    s.staleness = 0
        for p in playerBin:
            self.players.remove(p)
        for s in speciesBin:
            self.species.remove(s)

    def sortSpeciesByFitness(self):
        for s in self.species:
            s.sortPlayersByFitness()

        self.species.sort(key=operator.attrgetter("benchmarkFitness"), reverse=True)

    def nextGen(self):
        children = []

        # Clone of champion is added to each species
        for s in self.species:
            children.append(s.champion.clone())

        # Fill open player slots with children
        childrenPerSpecies = math.floor((self.size - len(self.species)) / len(self.species))
        for s in self.species:
            for i in range(0, childrenPerSpecies):
                children.append(s.offspring())

        while len(children)<self.size:
            children.append(self.species[0].offspring())

        self.players = []
        for child in children:
            self.players.append(child)
        self.generation += 1

    def extinct(self):
        extinct = True
        self.playersAlive = 0
        for p in self.players:
            if p.alive:
                self.playersAlive += 1
                extinct = False
        return extinct