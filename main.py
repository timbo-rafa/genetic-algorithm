#!/usr/bin/python3
from graph import Graph
from ga import GA
import itertools
import time
import multiprocessing as mp

GENERATIONS=1000

def run(
#parameters
  independent_populations, exchange_after, stop_after,
#graph parameters
  cities,
#ga parameters
  generations, population_size, elite_size, mutation_probability):
  if (independent_populations <= 0):
    raise ValueError("Number of independent populations must be positive.")
  if (exchange_after > generations):
    raise ValueError(
      "Number of generations needed to exchange top individuals must be smaller than \
      number of generations.")
  g = Graph(cities)
  ga = []
  for i in range(independent_populations):
    ga.append( GA(g, population_size=population_size, elite_size=elite_size,
      mutation_probability=mutation_probability) )
    if (i == 0):
      fittest = ga[i].fittest()
    elif( fittest.fitness > ga[i].fittest().fitness):
      fittest = ga[i].fittest()
  print("Start: Fitness {fitness}".format(fitness=fittest.fitness))

  start_time = time.clock()
  idle_time = 0
  for generation in range(generations):
    progress = False
    for pop in ga:
      pop.evolve()
      if (fittest.fitness > pop.fittest().fitness):
        progress = True
        fittest = pop.fittest()
        fittest_time = time.clock()
        print("[{time}] Generation {gen} Population {p} Fitness: {fit}"
          .format(time= fittest_time - start_time, p=ga.index(pop),
            gen=generation, fit=fittest.fitness))

    if ((generation % exchange_after) == 0 and independent_populations > 1 and generation):
      print("Gen {g}: Exchanging individuals".format(g=generation))
      for k, ga_k in enumerate(ga):
        fittest_individuals = []
        for i,ga_i in enumerate(ga):
          if (i != k):
            fittest_individuals.append(ga_i.fittest())
        ga_k.exchange(fittest_individuals)
      
    if (progress):
      idle_time = 0
    else:
      idle_time += 1

    if (idle_time == stop_after):
      print("Halting: No progress for {sa} generations. Best fitness {f}.".format(
        sa=stop_after, f=fittest.fitness))
      break #generation loop
  return fittest

if __name__ == '__main__':
  run(mp.cpu_count(), 50, 200, 200, 1000, 256, 10, 0.10)
  #run(mp.cpu_count(), 50, 200, 200, 1000, 700, 50, 0.20)
  #run(mp.cpu_count(), 50, 200, 200, 1000, 100, 5, 0.05)

# TO DO
# parallel populations
# swap best individuals after x generations
# STOP Criteria: N generations w/o improvement
