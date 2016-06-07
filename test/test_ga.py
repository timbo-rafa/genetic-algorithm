from nose.tools import assert_equal, assert_not_equal
from chromosome import Chromosome
from ga import GA
from graph import Graph
from itertools import repeat

GENERATIONS = 50

class Test_GA():
  _multiprocess_can_split_ = True

  def test_evolve_decreasing_fitness(self):
    self.g1 = Graph(n=100,source=99,save=False, option='generate')
    self.ga = GA(self.g1)
    self.generations = GENERATIONS
    for _ in repeat(None, self.generations):
      self.ga.evolve()
      f = 0
      for c in self.ga.population:
        assert f <= c.fitness
        f = c.fitness

  def test_population_size_large(self):
    self.g1 = Graph(n=100,source=99,save=False, option='generate')
    self.ga = GA(self.g1, population_size=500, elite_size=30)
    self.generations = GENERATIONS
    for _ in repeat(None, self.generations):
      self.ga.evolve()
      assert_equal(len(self.ga.population), self.ga.population_size)

  def test_population_size_small(self):
    self.g1 = Graph(n=100,source=99,save=False, option='generate')
    self.ga = GA(self.g1, population_size=50, elite_size=4)
    self.generations = GENERATIONS
    for _ in repeat(None, self.generations):
      self.ga.evolve()
      assert_equal(len(self.ga.population), self.ga.population_size)

  def test_best_fitness(self):
    self.g1 = Graph(n=100,source=99,save=False, option='generate')
    self.ga = GA(self.g1)
    self.generations = GENERATIONS * 1000
    self.ga.evolve()
    for _ in repeat(None, self.generations):
      f = self.ga.best_fitness()
      for c in self.ga.population[1:len(self.ga.population)]:
        assert f < c.fitness

  def debug(self):
    self.g = Graph(n=30, source=29, save=True, option='generate')
    self.ga = GA(self.g, population_size=30, elite_size=4)
    self.generations = GENERATIONS
    for generation in range(self.generations):
      self.ga.evolve()
      fittest = self.ga.fittest()
      print("Generation {g}, best fitness {f}".format(g=generation, f=fittest.fitness));
      for i, c in enumerate(self.ga.population):
        print("  Ind {i}: fitness: {f} path: {p}".format(i=i, f=c.fitness, p=c.path))
    assert True #False

