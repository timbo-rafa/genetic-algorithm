#!/usr/bin/python3
from ga_parallel import GA, MessageGA
import itertools
import time
#import multiprocessing as mp

GENERATIONS=1000
f=open("main.log", "w")


def qget(q, i):
  print("Main Queue({i})...".format(i=i), end="", file=f)
  r = q.get()
  print("{r}".format(r=r), file=f)
  return r

class State():
  def __init__(self, pqueue,
    independent_populations, exchange_after, stop_after, generations,
    latex, ga,
    progress=False, fittest=None, start_time=time.perf_counter()):

    self.progress = progress
    self.fittest = fittest
    self.start_time = start_time
    self.latex = latex
    self.ga = ga
    self.independent_populations = independent_populations
    self.exchange_after = exchange_after
    self.stop_after = stop_after
    self.generations = generations
    self.pqueue = pqueue
    self.update_fittest()

  def update_fittest(self):
    change = False
    #print("Fittest ", self.fitness)
    for i, q in enumerate(self.pqueue):
      #print("  ", self.fitness > pop.fittest().fitness, " ", pop.fittest().fitness)
      m = qget(q, i)
      try:
        self.fitness
      except:
        self.fitness = m.fitness + 1
      finally:
        if (self.fitness > m.fitness):
          change = True
          self.progress = True
          self.fittest_time = time.perf_counter()
          self.fitness = m.fitness
          self.fittest_pop = m.population
          self.generation = m.generation
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
        time=time.perf_counter() - self.start_time,start="Genesis", population_space="",
        fitness=self.fitness))
    else:
#Print latex header
      print("{time:>9} & {gen:<5} & {pop:<4} & {fitness:<8} //".format(
        time="Time", gen="Gen", pop="Pop", fitness="Fitness"))

  def print_state(self, generation):
    if (not self.latex):
      print("[{time:09.2f}] Generation {gen:5d}: Population {p:2d} Fitness: {fit:8d}"
        .format(time= self.fittest_time - self.start_time, p=self.fittest_pop,
          gen=generation, fit=self.fitness))
    else:
      print("{time:9.2f} & {gen:<5d} & {p:<4d} & {fit:<8d} //".format(
        time=self.fittest_time - self.start_time, gen=generation,
        p=self.fittest_pop, fit=self.fitness))

  def print_exchange(self, generation):
    if (not self.latex):
      print("[{time:09.2f}] Generation {g:5d}: Exchanged individuals".format(
        time=time.perf_counter() - self.start_time, g=generation))
    else:
      print("{time:9.2f} & {g:<5d} &      & Exchange //".
        format(time=time.perf_counter() - self.start_time, g=generation))

  def print_halt(self, generation):
    if (not self.latex):
      print("[{time_fill:*<9}] Halting: No progress for {sa} generations".format(
        time_fill="",sa=self.stop_after))
      print("[{time:09.2f}] Generation {g:5d}: {best_fitness:>21}: {f:8d}".format(
        time=time.perf_counter() - self.start_time , g=generation,
        best_fitness="Best Fitness", f=self.fitness))
    else:
      print("{time:9.2f} & {gen:<5d} & Halt & {f:<8d} //".format(
        time=time.perf_counter() - self.start_time, gen=generation, f=self.fitness))

  def print_stop(self, generation):
    if (not self.latex):
      print("[{time_fill:*<9}] Stopping: Iterated for {max_gen} generations".format(
        time_fill="", max_gen=self.generations))
      print("[{time:09.2f}] Generation {g:5d}: {best_fitness:>21}: {f:8d}".format(
        time=time.perf_counter() - self.start_time , g=generation,
        best_fitness="Best Fitness", f=self.fitness))
    else:
      print("{time:9.2f} & {gen:<5d} & Stop & {f:<8d} //".format(
        time=time.perf_counter() - self.start_time, gen=generation, f=self.fitness))

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
  exchange_after, stop_after, generations,
#graph parameters
  cities,
#ga parameters
  population_size, elite_size, mutation_probability,
  independent_populations=4, 
  verbose=False, latex=False):
#Checking for valid parameters
  if (exchange_after > generations):
    raise ValueError(
      "Number of generations needed to exchange top individuals must be smaller than " +
      "number of generations.")
  
#Print parameters  
  if (verbose):
    s.print_parameters()

#initialize algorithm
  ga = GA(cities, independent_populations,
    generations, exchange_after, stop_after,
    population_size=population_size,
    elite_size=elite_size, mutation_probability=mutation_probability)
  independent_populations = ga.independent_populations
#run it (non-blocking)
  proc, pqueue, departure_queues, arrival_queues = ga.evolve()

#state and printing
  s = State(pqueue, independent_populations, exchange_after, stop_after, generations, latex,
    ga,
    progress=False, start_time=time.perf_counter())

  s.print_header()
  idle_time = 0
#start evolution asynchronously
  for generation in range(s.generations):
    print("Main({g})...".format(g=generation), file=f)
    s.progress = False
#evolve population for one iteration
    #res = pool.map(evolve_map, s.ga)
    #for sga, r in zip(s.ga, res):
    #  sga.population = r
#check if a fitter individual was born and print its characteristics
    if (s.update_fittest()):
      s.print_state(generation)
    
#Exchange best individuals from each population if it is on proper generation
    if (((generation % exchange_after) == 0) and (independent_populations > 1)
        and generation):
      print("Main exchange...", end="", file=f)
      s.print_exchange(generation)
      for i in range(independent_populations):
        print("receiving immi from {i}...".format(i=i), end="", file=f)
        immigrant = departure_queues[i].get()
        print("Done", file=f)
        for j in range(independent_populations):
          if (i != j):
            arrival_queues[j].put(immigrant)
      
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

  for ql in [pqueue, departure_queues, arrival_queues]:
    for q in ql:
      q.close()
      q.join_thread()
  for p in proc:
    p.join()

  return s.fittest

if __name__ == '__main__':
  run(exchange_after=20, stop_after=1000, generations=900, cities=200,
    population_size=220, elite_size=20, mutation_probability=0.20)
  #run(50, 200, 1000, 200, 700, 50, 0.20)
  #run(50, 200, 1000, 200, 100, 5, 0.05)

# TO DO
# break run into functions
# parallel populations
