from nose.tools import assert_equal, assert_not_equal
from tsp.chromosome import Chromosome
from tsp.ga import GA
from tsp.graph import Graph
from itertools import repeat
import numpy as np

GENERATIONS = 50

class Test_GA():
  _multiprocess_can_split_ = True
  def setUp(self):
    self.g1 = Graph(n=100,source=99,save=False, option='generate')
    self.ga = GA(self.g1)
    self.generations = GENERATIONS

  def test_evolve_decreasing_fitness(self):
    for _ in repeat(None, self.generations):
      self.ga.evolve()
      f = 0
      for c in self.ga.population:
        assert f <= c.fitness
        f = c.fitness

  def test_population_size_large(self):
    for _ in repeat(None, self.generations):
      self.ga.evolve()
      assert_equal(len(self.ga.population), self.ga.population_size)

  def test_population_size_small(self):
    for _ in repeat(None, self.generations):
      self.ga.evolve()
      assert_equal(len(self.ga.population), self.ga.population_size)

  def test_best_fitness(self):
    self.ga.evolve()
    for _ in repeat(None, self.generations):
      f = self.ga.best_fitness()
      for c in self.ga.population[1:len(self.ga.population)]:
        assert f < c.fitness

  def test_exchange_size(self):
    self.ga.evolve()
    for _ in repeat(None, self.generations):
      cl = []
      for i in range(10):
        cl.append(Chromosome(99))
        cl[i].fitness = 500
      size = len(self.ga.population)
      self.ga.exchange(cl)
      assert_equal(size, len(self.ga.population))
  
  def test_exchange_fitness(self):
    self.ga.evolve()
    cl = [Chromosome(99)]
    size = len(self.ga.population)
    cl[0].fitness = 0
    self.ga.exchange(cl)
    assert_equal(0, self.ga.fittest().fitness)

  def test_simple_problem(self):
    g = Graph(n=10, source=9, save=False, option='generate')
    for i in range(10):
      for j in range(10):
        if (i != j):
          g.g[i][j]['weight'] = 10000
    g.g[9][0]['weight'] = 1000 
    g.g[8][9]['weight'] = 1000
    w = [1, 2, 4, 8, 16, 32, 64, 128]
    g.g[0][1]['weight'] = w[0]
    g.g[1][2]['weight'] = w[1]
    g.g[2][3]['weight'] = w[2]
    g.g[3][4]['weight'] = w[3]
    g.g[4][5]['weight'] = w[4]
    g.g[5][6]['weight'] = w[5]
    g.g[6][7]['weight'] = w[6]
    g.g[7][8]['weight'] = w[7]
    path = np.array([0,1,2,3,4,5,6,7,8])
    pathr = path[::-1]
    w.extend([1000, 1000])
    cost = sum(w)
    ga = GA(g)
    found = False
    for generations in range(500):
      ga.evolve()
      f = ga.fittest()
      if (f.fitness == cost):
        if (np.array_equal(f.path, path) or np.array_equal(f.path, pathr)):
          found = True
          break
    print("cost={c} fitness={f}".format(c=cost, f=f.fitness))
    assert found
    pass

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

