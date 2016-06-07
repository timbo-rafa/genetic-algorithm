#!/usr/bin/env python

import random
from chromosome import Chromosome
from graph import Graph #
import numpy as np

POPULATION_SIZE=300
P_ELITE=0.10
MUTATION_PROBABILITY=0.10
P_ELITE_OFFSPRING=0.70
ELITE_SIZE=10 # number of best individuals that will survive through generations

class GA():
  def __init__(self, g, population_size=POPULATION_SIZE, p_elite=P_ELITE,
    p_elite_offspring=P_ELITE_OFFSPRING, elite_size=ELITE_SIZE,
    mutation_probability=MUTATION_PROBABILITY):
    self.g = g
    self.population_size = population_size
    self.p_elite = p_elite
    self.elite_size = elite_size
    if (self.elite_size >= self.population_size):
      raise ValueError("Elite size({e}) must be smaller than population size({p})."
          .format(e=self.elite_size,p=self.population_size))
    if (self.elite_size < 1):
      raise ValueError("Elite size must be positive.")
    self.p_elite_offspring = p_elite_offspring
    self.mutation_probability = mutation_probability
    self.population = [Chromosome(self.g.n - 1, random=True) for _ in range(population_size)]
    self.calculate_fitness()

  def fitness(self, chromosome):
    return self.g.path_cost(chromosome.path)

  def calculate_fitness(self):
    self.fitness_total = 0
    self.weighted_total = 0.0
    for c in self.population:
      c.fitness = self.fitness(c)
      c.weighted_fitness = 1.0/c.fitness
      self.fitness_total += c.fitness
      self.weighted_total += c.weighted_fitness

  def weighted_choice(self):
    choice = random.uniform(0, self.weighted_total)
    for c in self.population:
      if choice < c.weighted_fitness:
        return c
      choice -= c.weighted_fitness
    return self.population[0] 

  def fittest(self):
    return self.population[0]

  def evolve(self):
    """ Evolve the population for one iteration """
    self.new_population = []

    #elitism
    current = self.population[0]
    self.new_population.append(current)
    elite_n = 1
    i = 1
    while (elite_n < self.elite_size):
      if (i < self.population_size):
        if (current != self.population[i]):
          self.new_population.append(self.population[i])
          current = self.population[i]
          elite_n += 1
        i += 1
      else:
        elite_n = self.elite_size

    for _ in range(self.population_size//2 - self.elite_size//2):
      #reproduce
      p1 = self.weighted_choice()
      p2 = self.weighted_choice()
      child1, child2 = p1.crossover(p2)
      #mutate
      if (random.random() < self.mutation_probability ):
        child1.mutate()
      if (random.random() < self.mutation_probability ):
        child2.mutate()
      self.new_population.append(child1)
      self.new_population.append(child2)
    #update solution
    self.population = self.new_population
    self.calculate_fitness()
    #fittest solution in self.population[0]
    self.population.sort(key=lambda x: x.fitness)
    return self.fittest()

  def best_fitness(self):
    return self.fittest().fitness
