#!/usr/bin/env python

import random
from chromosome import Chromosome
from graph import Graph #
from itertools import repeat
import numpy as np
import multiprocessing as mp

POPULATION_SIZE=300
P_ELITE=0.10
MUTATION_PROBABILITY=0.10
P_ELITE_OFFSPRING=0.70
ELITE_SIZE=10 # number of best individuals that will survive through generations

class GA():
  def __init__(self, g, population_size=POPULATION_SIZE, p_elite=P_ELITE,
    p_elite_offspring=P_ELITE_OFFSPRING, elite_size=ELITE_SIZE,
    mutation_probability=MUTATION_PROBABILITY,
    number_of_cores=mp.cpu_count()):
    self.g = g
    self.population_size = population_size
    self.p_elite = p_elite
    self.elite_size = elite_size
    if (self.elite_size >= self.population_size):
      raise ValueError("Elite size({e}) must be smaller than population size({p})."
          .format(e=self.elite_size,p=self.population_size))
    if (self.elite_size < 1):
      raise ValueError("Elite size must be positive.")
    #if (number_of_cores == 1):
    #  raise ValueError("Number of cores({c}) must be greater than 1.".format(c=number_of_cores))
    if ((population_size - elite_size) % (2 * number_of_cores) != 0):
      raise ValueError(("Population size({ps}) - Elite size({es}) must be a multiple of " +
        "2*number_of_cores=({dc}). Population size - elite size  % {dc} = {r}").format(
        ps=population_size, es=elite_size, dc=2*number_of_cores,
        r=(population_size - elite_size) % (2 * number_of_cores)))
    self.p_elite_offspring = p_elite_offspring
    self.mutation_probability = mutation_probability
    self.number_of_cores = number_of_cores
    #self.consumer_queue = mp.Queue()
    #self.pool = mp.Pool(processes=number_of_cores)
    self.population = [Chromosome(self.g.n -1, random=True) for _ in repeat(None,population_size)]
    self.calculate_fitness()

  def fitness(self, chromosome):
    return self.g.path_cost(chromosome.path)

  def calculate_fitness(self):
    self.fitness_total = 0
    self.weighted_total = 0.0
#paralelizar
    for c in self.population:
      c.fitness = self.fitness(c)
      c.weighted_fitness = 1.0/c.fitness
      self.fitness_total += c.fitness
      self.weighted_total += c.weighted_fitness

  def weighted_choice(self):
    choice = random.uniform(0, self.weighted_total)
#paralelizar dando n chromosomos para cada processo
    for c in self.population:
      if choice < c.weighted_fitness:
        return c
      choice -= c.weighted_fitness
    return self.population[0] 

  def weighted_choice_producer(self, q, chunksize):
    """Asynchronous producer function that chooses n chromosomes from population"""
    #print("Weighted choice producer self={s} q={q} chunksize={c}"
    #  .format(s=self, q=q, c=chunksize))
    for _ in repeat(None, chunksize):
      #c1 = self.pool.apply_async(self.weighted_choice, args=(self,))
      #c2 = self.pool.apply_async(self.weighted_choice, args=(self,))
      #t = (c1.get(), c2.get())
      t = (self.weighted_choice(), self.weighted_choice())
      q.put(t)
    #self.consumer_queue.close()
    #self.consumer_queue.join_thread()

  def evolve_consumer(self, q, chunksize):
    """Asynchronous consumer function that reproduces and mutates the population"""
    new_pop = []
    #print("evolve consumer self={s} q={q} chunksize={c}".format(s=self, q=q, c=chunksize))
    for _ in repeat(None, chunksize):
      chromosome_pair = q.get()
#reproduce
      child1, child2 = chromosome_pair[0].crossover(chromosome_pair[1])
#mutate
      if (random.random() < self.mutation_probability ):
        child1.mutate()
      if (random.random() < self.mutation_probability ):
        child2.mutate()
      new_pop.append(child1)
      new_pop.append(child2)
    return new_pop

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

    total = (self.population_size - self.elite_size)//2
    chunksize = total//self.number_of_cores
    prod = []
    consumer_queue = mp.Manager().Queue()
    pool = mp.Pool()
    for _ in repeat(None, self.number_of_cores):
      prod.append(pool.apply_async(self.weighted_choice_producer,
        args=(consumer_queue, chunksize,)))
    
    cons = []    
    for _ in repeat(None, self.number_of_cores):
      cons.append(pool.apply_async(self.evolve_consumer,
        args=(consumer_queue, chunksize) ) )

    pool.close()
    self.population = self.new_population
    for c in cons:
      self.population.extend(c.get())

    #update solution
    self.calculate_fitness()
    #fittest solution in self.population[0]
    self.population.sort(key=lambda x: x.fitness)
    #exit nicely waiting for async stuff (which should be done)
    for p in prod:
      p.wait()
    pool.join()
    #consumer_queue.close()
    #consumer_queue.join_thread()

    return self.population

  def best_fitness(self):
    return self.fittest().fitness
    
  def exchange(self, incomers):
    self.population.extend(incomers)
    self.population.sort(key=lambda x: x.fitness)
    del self.population[len(self.population) - len(incomers) - 3: len(self.population) - 3]
