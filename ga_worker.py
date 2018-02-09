#!/usr/bin/env python

import random
from itertools import repeat

def weighted_choice(weighted_total, population):
  choice = random.uniform(0, weighted_total)
  #paralelizar dando n chromosomos para cada processo
  for c in population:
    if choice < c.weighted_fitness:
      return c
    choice -= c.weighted_fitness
  return population[0] 

def weighted_choice_producer(q, chunksize, weighted_total, population, wid):
  """Asynchronous producer function that chooses n chromosomes from population
    q: queue with chosen chromosomes
    chunksize: number of chromosomes to be picked
    weighted_total: sum of fitness weights. In probability this usually sums up to 1.0.
    population: array of chromosomes to draw from
    wid: worker id."""

  for _ in repeat(None, chunksize):
    t = (weighted_choice(weighted_total, population),
         weighted_choice(weighted_total, population))
    q.put(t)

def evolve_consumer(q, chunksize, mutation_probability, wid):
  """Asynchronous consumer function that reproduces and mutates the population
  producing _chunksize_ individuals
  q: queue with chromosomes to be consumed and evolved.
  chunksize: number of pairs of chromosomes to be consumed and evolved.
  mutation_probability: probability that a chromosome will mutate.
  wid: worker id."""
  new_pop = []
  for _ in repeat(None, chunksize):
    chromosome_pair = q.get()
    #reproduce
    child1, child2 = chromosome_pair[0].crossover(chromosome_pair[1])
    #mutate
    if (random.random() < mutation_probability ):
      child1.mutate()
    if (random.random() < mutation_probability ):
      child2.mutate()
    # Erase fitness to be updated later
    child1.fitness = None
    child2.fitness = None
    new_pop.append(child1)
    new_pop.append(child2)

  return new_pop
