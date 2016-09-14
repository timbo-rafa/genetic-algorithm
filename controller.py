from ga_parallel import GA, MessageGA
from state import State
import itertools
import time

def run(
#parameters
  exchange_after, stop_after, generations,
#graph parameters
  cities,
#ga parameters
  population_size, elite_size, mutation_probability,
  independent_populations, number_workers, 
  verbose=False, latex=False):
  """Outermost loop function that evolves the genetic algorithm,
  delegating output to state and specifics to the GA class"""
#Checking for valid parameters
  if (exchange_after > generations):
    raise ValueError(
      "Number of generations needed to exchange top individuals must be smaller than " +
      "number of generations.")

#initialize algorithm
  ga = GA(cities, independent_populations, number_workers,
    generations, exchange_after, stop_after,
    population_size=population_size,
    elite_size=elite_size, mutation_probability=mutation_probability)
  independent_populations = ga.independent_populations
#run evolution asynchronously (non-blocking)
  proc, pqueue, departure_queues, arrival_queues = ga.evolve()

#state and printing
  s = State(pqueue, independent_populations, population_size, elite_size, mutation_probability,
    exchange_after, stop_after, generations, latex, ga,
    progress=False, start_time=time.perf_counter())
  
#Print parameters  
  #if (verbose):
  s.print_parameters()

  s.print_header()
  idle_time = 0
  for generation in range(s.generations):
#display population progress for one iteration
    s.progress = False
#check if a fitter individual was born and print its characteristics
    if (s.update_fittest()):
      s.print_state(generation)
    
#Exchange best individuals from each population if it is on proper generation
    if (((generation % exchange_after) == 0) and (independent_populations > 1)
        and generation):
      s.print_exchange(generation)
      for i in range(independent_populations):
        immigrant = departure_queues[i].get()
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
    s.print_solution()

  for ql in [pqueue, departure_queues, arrival_queues]:
    for q in ql:
      q.close()
      q.join_thread()
  for p in proc:
    p.join()

  return s.fittest
