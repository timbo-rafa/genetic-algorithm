#!/usr/bin/python3
from graph import Graph
from ga_parallel import GA
import itertools
import time
import multiprocessing as mp

GENERATIONS=1000

class State():
  def __init__(self,
    independent_populations, exchange_after, stop_after, generations,
    latex, ga=[],
    progress=False, fittest=None, start_time=time.clock()):

    self.progress = progress
    self.fittest = fittest
    self.start_time = start_time
    self.latex = latex
    self.ga = ga
    self.independent_populations = independent_populations
    self.exchange_after = exchange_after
    self.stop_after = stop_after
    self.generations = generations
    if (isinstance(self.ga, list)):
      if (len(self.ga)):
        self.fittest = self.ga[0].fittest()
        self.update_fittest()

  def update_fittest(self):
    change = False
    #print("Fittest ", self.fittest.fitness)
    for pop in self.ga:
      #print("  ", self.fittest.fitness > pop.fittest().fitness, " ", pop.fittest().fitness)
      if (self.fittest.fitness > pop.fittest().fitness):
        change = True
        self.progress = True
        self.fittest_time = time.clock()
        self.fittest = pop.fittest()
        self.fittest_pop = self.ga.index(pop)
    return change

  def print_parameters(self):
    if(not self.latex):
      print("Number of Independent Populations={nip}".format(nip=independent_populations))
      print("Generations before exchanging top individuals={e}".format(e=exchange_after))
      print("Maximum number of idle generations={sa}".format(sa=stop_after))
      print("Maximum number of generations={max}".format(max=generations))
      print("Population size={ps}".format(ps=population_size))
      print("Elite size={es}".format(es=elite_size))
      print("Mutation probability={mp}".format(mp=mutation_probability))
    else:
      print("Independent Populations & {ip} //".format(ip=independent_populations))
      print("Exchange after & {e} //".format(e=exchange_after))
      print("Stop after & {sa} //".format(sa=stop_after))
      print("Max \# generations & {max} //".format(max=generations))
      print("Population size & {ps} //".format(ps=population_size))
      print("Elite size & {es} //".format(es=elite_size))
      print("Mutation probability & {mp} //".format(mp=mutation_probability))

  def print_header(self):
    if (not self.latex):
#Print starting fitness
      print("[{time:09.2f}] {start:<16}: {population_space:13} Fitness: {fitness:8d}".format(
        time=time.clock() - self.start_time,start="Genesis", population_space="",
        fitness=self.fittest.fitness))
    else:
#Print latex header
      print("{time:>9} & {gen:<5} & {pop:<4} & {fitness:<8} //".format(
        time="Time", gen="Gen", pop="Pop", fitness="Fitness"))

  def print_state(self, generation):
    if (not self.latex):
      print("[{time:09.2f}] Generation {gen:5d}: Population {p:2d} Fitness: {fit:8d}"
        .format(time= self.fittest_time - self.start_time, p=self.fittest_pop,
          gen=generation, fit=self.fittest.fitness))
    else:
      print("{time:9.2f} & {gen:<5d} & {p:<4d} & {fit:<8d} //".format(
        time=self.fittest_time - self.start_time, gen=generation,
        p=self.fittest_pop, fit=self.fittest.fitness))

  def print_exchange(self, generation):
    if (not self.latex):
      print("[{time:09.2f}] Generation {g:5d}: Exchanged individuals".format(
        time=time.clock() - self.start_time, g=generation))
    else:
      print("{time:9.2f} & {g:<5d} &      & Exchange //".
        format(time=time.clock() - self.start_time, g=generation))

  def print_halt(self, generation):
    if (not self.latex):
      print("[{time_fill:*<9}] Halting: No progress for {sa} generations".format(
        time_fill="",sa=self.stop_after))
      print("[{time:09.2f}] Generation {g:5d}: {best_fitness:>21}: {f:8d}".format(
        time=time.clock() - self.start_time , g=generation,
        best_fitness="Best Fitness", f=self.fittest.fitness))
    else:
      print("{time:9.2f} & {gen:<5d} & Halt & {f:<8d} //".format(
        time=time.clock() - self.start_time, gen=generation, f=self.fittest.fitness))

  def print_stop(self, generation):
    if (not self.latex):
      print("[{time_fill:*<9}] Stopping: Iterated for {max_gen} generations".format(
        time_fill="", max_gen=self.generations))
      print("[{time:09.2f}] Generation {g:5d}: {best_fitness:>21}: {f:8d}".format(
        time=time.clock() - self.start_time , g=generation,
        best_fitness="Best Fitness", f=self.fittest.fitness))
    else:
      print("{time:9.2f} & {gen:<5d} & Stop & {f:<8d} //".format(
        time=time.clock() - self.start_time, gen=generation, f=self.fittest.fitness))

  def print_solution(self, source):
    path_str = "{n}".format(n=source)
    s = ">{n}"
    for city in self.fittest:
      path_str += s.format(n=city)
    path_str += s.format(n=source)
    print(path_str)

def evolve_map(ga):
  return ga.evolve()

def run(
#parameters
  independent_populations, exchange_after, stop_after, generations,
#graph parameters
  cities,
#ga parameters
  population_size, elite_size, mutation_probability,
  verbose=False, latex=False):
#Checking for valid parameters
  if (independent_populations <= 0):
    raise ValueError("Number of independent populations must be positive.")
  if (exchange_after > generations):
    raise ValueError(
      "Number of generations needed to exchange top individuals must be smaller than " +
      "number of generations.")
  
#Print parameters  
  if (verbose):
    s.print_parameters()

  g = Graph(cities)
  ga = [GA(g, population_size=population_size, elite_size=elite_size,
    mutation_probability=mutation_probability, number_of_cores=independent_populations)
    for _ in range(independent_populations)]
#initialize all populations
  s = State(independent_populations, exchange_after, stop_after, generations, latex,
    ga,
    progress=False, start_time=time.clock())

  s.print_header()
  pool = mp.Pool(processes=independent_populations)
  idle_time = 0
#loop for generations
  for generation in range(s.generations):
    s.progress = False
#evolve population for one iteration
    for pop in s.ga:
      pop.evolve()
    #res = pool.map(evolve_map, s.ga)
    #for sga, r in zip(s.ga, res):
    #  sga.population = r
#check if a fitter individual was born and print its characteristics
    if (s.update_fittest()):
      s.print_state(generation)
    
#Exchange best individuals from each population if it is on proper generation
    if ((generation % exchange_after) == 0 and independent_populations > 1 and generation):
      s.print_exchange(generation)
      for k, ga_k in enumerate(s.ga):
        fittest_individuals = []
        for i,ga_i in enumerate(s.ga):
          if (i != k):
            fittest_individuals.append(ga_i.fittest())
        ga_k.exchange(fittest_individuals)
      
    if (s.progress):
      idle_time = 0
    else:
      idle_time += 1
    if (idle_time == s.stop_after):
      break #generation loop

# Figure out the stop criteria and print stuff accordingly
# Idle for set generations
  if (idle_time == stop_after):
    s.print_halt(generation)

# Max number of generations reached
  if (generation + 1 == generations):
    s.print_stop(generation)

  if (verbose):
    s.print_solution(g.source)
  pool.close()
  pool.join()
  return s.fittest

if __name__ == '__main__':
  #run(indep_pop, exchange, stop, gen, cities, pop_size, elite_size, mut_p
  run(mp.cpu_count(), 80, 200, 100, 200, 170, 10, 0.10)
  #run(mp.cpu_count(), 50, 200, 1000, 200, 700, 50, 0.20)
  #run(mp.cpu_count(), 50, 200, 1000, 200, 100, 5, 0.05)

# TO DO
# break run into functions
# parallel populations
