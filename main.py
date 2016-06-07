#!/usr/bin/python3
from graph import Graph
from ga import GA
import time

NUMBER_OF_CITIES=200
GENERATIONS=1000

def run(generations, population_size, elite_size, mutation_probability):
  source_node = NUMBER_OF_CITIES - 1
  g = Graph(NUMBER_OF_CITIES)
  ga = GA(g, population_size=population_size, elite_size=elite_size,
      mutation_probability=mutation_probability)
  fittest = ga.fittest()
  current = fittest
  print("Start: Fitness {fitness}".format(fitness=fittest.fitness))

  start_time = time.clock()
  for generation in range(generations):
    ga.evolve()
    current = ga.fittest()
    if (current.fitness < fittest.fitness):
      current_time = time.clock()
      fittest = current
      #print("Generation {gen} & Fitness: {fit} after {time}"
      #print("{gen} & {fit} & {time} \\\\"
      #  .format(gen=generation, fit=fittest.fitness, time=current_time - start_time))
    print("Generation {gen} & Fitness: {fit}"
      .format(gen=generation, fit=fittest.fitness))

if __name__ == '__main__':
  run(300, 256, 10, 0.10)
  #run(500, 700, 50, 0.20)
  #run(600, 100, 5, 0.05)

# TO DO
# parallel populations
# swap best individuals after x generations
# STOP Criteria: N generations w/o improvement
