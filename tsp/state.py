import time

class State():
  def __init__(self, pqueue,
    independent_populations, population_size, elite_size, mutation_probability,
    exchange_after, generations, latex, ga,
    progress=False, fittest=None, start_time=time.perf_counter()):

    self.progress = progress
    self.fittest = fittest
    self.start_time = start_time
    self.latex = latex
    self.ga = ga
    self.independent_populations = independent_populations
    self.population_size = population_size
    self.elite_size = elite_size
    self.mutation_probability = mutation_probability
    self.exchange_after = exchange_after
    self.generations = generations
    self.pqueue = pqueue
    self.update_fittest()

  def update_fittest(self):
    change = False
    for q in self.pqueue:
      m = q.get()
      try:
        self.fitness
      except:
        self.fitness = m.fitness + 1
      finally:
        try:
          if (self.fitness > m.fitness):
            change = True
            self.progress = True
            self.fittest_time = time.perf_counter()
            self.fitness = m.fitness
            self.fittest_pop = m.population
            self.generation = m.generation
        except AttributeError:
          print("m={m}".format(m=m))
          raise
    return change

  def print_parameters(self):
    if(not self.latex):
      print("Number of Independent Populations={nip}".format(nip=self.independent_populations))
      print("Generations before exchanging top individuals={e}".format(e=self.exchange_after))
      print("Maximum number of generations={max}".format(max=self.generations))
      print("Population size={ps}".format(ps=self.population_size))
      print("Elite size={es}".format(es=self.elite_size))
      print("Mutation probability={mp}".format(mp=self.mutation_probability))
    else:
      print("Independent Populations & {ip} //".format(ip=self.independent_populations))
      print("Exchange after & {e} //".format(e=self.exchange_after))
      print("Max \# generations & {max} //".format(max=self.generations))
      print("Population size & {ps} //".format(ps=self.population_size))
      print("Elite size & {es} //".format(es=self.elite_size))
      print("Mutation probability & {mp} //".format(mp=self.mutation_probability))

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

  def print_solution(self):
    fittest = None
    for q in self.pqueue:
      qfitness = q.get()
      qfittest = q.get()
      if (qfitness == self.fitness):
          fittest = qfittest
    path_str = "{n}".format(n=fittest[0])
    s = ">{n}"
    for city in fittest[1:]:
      path_str += s.format(n=city)
    print(path_str)
