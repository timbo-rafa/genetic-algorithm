  def calculate_fitness(self):
    self.fitness_total = 0
    self.weighted_total = 0.0
    for c in self.population:
      try:
        c.fitness = self.fitness(c)
      except KeyError:
        print("c path={p}".format(p=c.path))
        print("c path sorted={s}".format(s=np.sort(c.path)))
        raise
      c.weighted_fitness = 1.0/c.fitness
      self.fitness_total += c.fitness
      self.weighted_total += c.weighted_fitness
