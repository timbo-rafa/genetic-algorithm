#!/usr/bin/python3
from graph import Graph
from ga import GA
import itertools
import time
import multiprocessing as mp

GENERATIONS=1000

def run(
#parameters
  independent_populations, exchange_after, stop_after, generations,
#graph parameters
  cities,
#ga parameters
  population_size, elite_size, mutation_probability, latex=False):
  if (independent_populations <= 0):
    raise ValueError("Number of independent populations must be positive.")
  if (exchange_after > generations):
    raise ValueError(
      "Number of generations needed to exchange top individuals must be smaller than \
      number of generations.")
  
  g = Graph(cities)
  ga = []
#initialize all populations
  for i in range(independent_populations):
    ga.append( GA(g, population_size=population_size, elite_size=elite_size,
      mutation_probability=mutation_probability) )
    if (i == 0):
      fittest = ga[i].fittest()
    elif( fittest.fitness > ga[i].fittest().fitness):
      fittest = ga[i].fittest()

  start_time = time.clock()
  if (not latex):
    print("[{time:09.2f}] {start:<16}: {population_space:13} Fitness: {fitness:8d}".format(
      time=time.clock() - start_time,start="Genesis", population_space="",
      fitness=fittest.fitness))
  else:
    print("{time:>9} & {gen:<5} & {pop:<4} & {fitness:<8} //".format(
      time="Time", gen="Gen", pop="Pop", fitness="Fitness"))

  idle_time = 0
#loop for generations
  for generation in range(generations):
    progress = False
    for pop in ga:
#evolve population for one iteration
      pop.evolve()
#check if a fitter individual was born
      if (fittest.fitness > pop.fittest().fitness):
        progress = True
        fittest = pop.fittest()
        fittest_time = time.clock()
        if (not latex):
          print("[{time:09.2f}] Generation {gen:5d}: Population {p:2d} Fitness: {fit:8d}"
            .format(time= fittest_time - start_time, p=ga.index(pop),
              gen=generation, fit=fittest.fitness))
        else:
          print("{time:9.2f} & {gen:<5d} & {p:<4d} & {fit:<8d} //".format(
            time=fittest_time - start_time, gen=generation, p=ga.index(pop), fit=fittest.fitness))

#Exchange best individuals from each population if it is on proper generation
    if ((generation % exchange_after) == 0 and independent_populations > 1 and generation):
      if (not latex):
        print("[{time:09.2f}] Generation {g:5d}: Exchanged individuals".format(
          time=time.clock() - start_time, g=generation))
      else:
        print("{time:9.2f} & {g:<5d} &      & Exchange //".
          format(time=time.clock() - start_time, g=generation))
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
      break #generation loop

# Figure out the stop criteria and print stuff accordingly
# Idle for set generations
  if (idle_time == stop_after):
    if (not latex):
      print("[{time_fill:*<9}] Halting: No progress for {sa} generations".format(
        time_fill="",sa=stop_after))
      print("[{time:09.2f}] Generation {g:5d}: {best_fitness:>21}: {f:8d}".format(
        time=time.clock() - start_time , g=generation,
        best_fitness="Best Fitness", f=fittest.fitness))
    else:
      print("{time:9.2f} & {gen:<5d} & Halt & {f:<8d} //".format(
        time=time.clock() - start_time, gen=generation, f=fittest.fitness))

# Max number of generations reached
  if (generation + 1 == generations):
    if (not latex):
      print("[{time_fill:*<9}] Stopping: Iterated for {max_gen} generations".format(
        time_fill="", max_gen=generations))
      print("[{time:09.2f}] Generation {g:5d}: {best_fitness:>21}: {f:8d}".format(
        time=time.clock() - start_time , g=generation,
        best_fitness="Best Fitness", f=fittest.fitness))
    else:
      print("{time:9.2f} & {gen:<5d} & Stop & {f:<8d} //".format(
        time=time.clock() - start_time, gen=generation, f=fittest.fitness))
  return fittest

if __name__ == '__main__':
  run(mp.cpu_count()//2, 10, 20, 100, 200, 256, 10, 0.10)
  #run(mp.cpu_count(), 50, 200, 1000, 200, 700, 50, 0.20)
  #run(mp.cpu_count(), 50, 200, 1000, 200, 100, 5, 0.05)

# TO DO
# parallel populations
# print parameters
