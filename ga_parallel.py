#!/usr/bin/env python

import random
from chromosome import Chromosome
from graph import Graph #
from itertools import repeat
import numpy as np
import multiprocessing as mp
import os

POPULATION_SIZE=300
P_ELITE=0.10
MUTATION_PROBABILITY=0.10
P_ELITE_OFFSPRING=0.70
ELITE_SIZE=10 # number of best individuals that will survive through generations

def qput(q, item, f2):
  print("Worker Producer...", end="", file=f2)
  q.put(item)
  print("  {item}".format(item=item), file=f2)

def weighted_choice(weighted_total, population):
  choice = random.uniform(0, weighted_total)
#paralelizar dando n chromosomos para cada processo
  for c in population:
    if choice < c.weighted_fitness:
      return c
    choice -= c.weighted_fitness
  return population[0] 

def weighted_choice_producer_worker(q, chunksize, weighted_total, population, wid):
  """Asynchronous producer function that chooses n chromosomes from population"""
  #print("Weighted choice producer self={s} q={q} chunksize={c}"

  f = open("wp" + str(wid) + ".log", "w")
  for _ in repeat(None, chunksize):
    t = (weighted_choice(weighted_total, population),
         weighted_choice(weighted_total, population))
    qput(q, t, f)
    #q.put(t)
  print("Finished", file=f)

def qget(q, f):
  print("worker Consumer...", end="", file=f)
  r = q.get()
  print(" {r}".format(r=r), file=f)
  return r

def evolve_consumer_worker(q, chunksize, mutation_probability, wid):
  """Asynchronous consumer function that reproduces and mutates the population
  producing _chunksize_ individuals"""
  new_pop = []
  f = open("wc" + str(wid) + ".log", "w")
  #print("evolve consumer self={s} q={q} chunksize={c}".format(s=self, q=q, c=chunksize))
  for _ in repeat(None, chunksize):
    chromosome_pair = qget(q, f)
#reproduce
    child1, child2 = chromosome_pair[0].crossover(chromosome_pair[1])
#mutate
    if (random.random() < mutation_probability ):
      child1.mutate()
    if (random.random() < mutation_probability ):
      child2.mutate()
    new_pop.append(child1)
    new_pop.append(child2)

  print("Finished", file=f)
  return new_pop

class MessageGA():
  def __init__(self, generation, population, fittest_fitness, pid=-1):
    self.generation = generation
    self.population = population
    self.fitness = fittest_fitness
    self.pid = pid
    #print("Creation", self)

  def __str__(self):
    if (self.pid != -1):
      r = "pid({pid}): gen({gen}) pop({pop}) fit={fit}".format(
        pid=self.pid, gen=self.generation, pop=self.population, fit=self.fitness)
    else:
      r = "gen({gen}) pop({pop}) fit={fit}".format(
        pid=self.pid, gen=self.generation, pop=self.population, fit=self.fitness)
    #print(self.pid, self.generation, self.population, self.fitness)
    return r

class GA():
  def __init__(self, cities, independent_populations,
      generations, exchange_after, stop_after,
      population_size=POPULATION_SIZE, p_elite=P_ELITE,
      p_elite_offspring=P_ELITE_OFFSPRING, elite_size=ELITE_SIZE,
      mutation_probability=MUTATION_PROBABILITY):
    self.population_size = population_size
    self.p_elite = p_elite
    self.elite_size = elite_size
    self.p_elite_offspring = p_elite_offspring
    self.mutation_probability = mutation_probability
    self.chromosome_size = cities - 1
    self.generations = generations
    self.exchange_after = exchange_after
    self.stop_after = stop_after
    if (independent_populations == None):
      self.independent_populations = mp.cpu_count()
    else:
      self.independent_populations = independent_populations
    if (self.elite_size >= self.population_size):
      raise ValueError("Elite size({e}) must be smaller than population size({p})."
          .format(e=self.elite_size,p=self.population_size))
    if (self.elite_size < 1):
      raise ValueError("Elite size must be positive.")
    if ((population_size - elite_size) % (2 * self.independent_populations) != 0):
      raise ValueError(("Population size({ps}) - Elite size({es}) must be a multiple of " +
        "2*independent_populations=({dc}). Population size - elite size  % {dc} = {r}").format(
        ps=population_size, es=elite_size, dc=2*self.independent_populations,
        r=(population_size - elite_size) % (2 * self.independent_populations)))

  def __init_per_process__(self):
    self.g = Graph(self.chromosome_size + 1)
    self.population = [
      Chromosome(self.chromosome_size, random=True) for _ in repeat(None,self.population_size)]
    self.calculate_fitness()
    #self.pool = mp.Pool(processes=self.independent_populations)
    #self.consumer_queue = mp.Queue()

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

  def fittest(self):
    return self.population[0]

  def evolve_process(self, pid,
      output_queue,     #output parameters to print status of each queue
      departure_queue,  #queue where we send the best individuals to exchange w foreign pop
      arrival_queue):   #queue where this population receives new individuals

    self.__init_per_process__()
    output_queue.put(MessageGA(-1, pid, self.best_fitness()))
    total = (self.population_size - self.elite_size)//2
    chunksize = total//self.independent_populations
    idle_time = 0
    f2 = open(str(pid) + ".log", "w")
    consumer_queue = mp.Queue()
    for gen in range(self.generations):
      progress = False
      new_population = []
      current = self.population[0]
      new_population.append(current)
      elite_n = 1
      i = 1
      while (elite_n < self.elite_size):
        if (i < self.population_size):
          if (current != self.population[i]):
            new_population.append(self.population[i])
            current = self.population[i]
            elite_n += 1
          i += 1
        else:
          elite_n = self.elite_size
      
      print("gen({g}) started>".format(g=gen), end="", file=f2)
      #prod = pool.apply_async(weighted_choice_producer_worker,
      #  args=(consumer_queue, total, self.weighted_total, self.population, pid))
      prod = mp.Process(target=weighted_choice_producer_worker, 
        args=(consumer_queue, total, self.weighted_total, self.population, pid))
      prod.start()
      print("Producer Started>", end="", file=f2)
      
      reproduced_and_mutated_individuals = evolve_consumer_worker(
        consumer_queue, total, self.mutation_probability, pid)
      new_population.extend(reproduced_and_mutated_individuals)

      print("Consumer returned>", end="", file=f2)
      #exit nicely waiting for async stuff (which should be done)
      self.population = new_population

      #update solution
      self.calculate_fitness()
      #fittest solution in self.population[0]
      self.population.sort(key=lambda x: x.fitness)
      fittest = self.fittest()

      qput(output_queue,MessageGA(gen, pid, self.best_fitness()), f2)
      #output_queue.put(MessageGA(gen, pid, self.best_fitness()))

      if ((gen % self.exchange_after) == 0 and self.independent_populations > 1 and gen):
        print("Exchange...", end="", file=f2)
        departure_queue.put(self.fittest())
        print("receiving immis...", end="", file=f2)
        incomers = [arrival_queue.get() for _ in repeat(None, self.independent_populations - 1)]
        print("Done", file=f2)
        self.exchange(incomers)

      prod.join()
      print("Joined producer>", end="", file=f2)
      print("gen({g}) ended".format(g=gen), file=f2)

      if (self.fittest() != fittest):
        idle_time = 0
      else:
        idle_time += 1
      if (idle_time == self.stop_after):
        print("Breaking(idle={i})".format(i=idle_time))
        break #generation loop

      
    consumer_queue.close()
    output_queue.close()
    arrival_queue.close()
    departure_queue.close()
    output_queue.join_thread()
    arrival_queue.join_thread()
    departure_queue.join_thread()
    return self.population

  def evolve(self, independent_populations=None,
      generations=None):
    """ Evolve the population asynchronously, sending generation status through the queues """
    if independent_populations==None:
      independent_populations = self.independent_populations
    if generations==None:
      generations = self.generations

    proc = []
    pop_queues = []
    departure_queues = [] 
    arrival_queues = []
    for  i in range(independent_populations):
      dq = mp.Queue()
      aq = mp.Queue()
      q = mp.Queue()
      p = mp.Process(target=self.evolve_process, args=(i, q, dq, aq))
      p.start()
      pop_queues.append(q)
      departure_queues.append(dq)
      arrival_queues.append(aq)
      proc.append(p)
    return proc, pop_queues, departure_queues, arrival_queues

  def best_fitness(self):
    return self.fittest().fitness
    
  def exchange(self, incomers):
    self.population.extend(incomers)
    self.population.sort(key=lambda x: x.fitness)
    del self.population[len(self.population) - len(incomers) - 3: len(self.population) - 3]