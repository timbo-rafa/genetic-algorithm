from tsp.ga import Chromosome
from nose.tools import assert_equal, assert_not_equal
import numpy as np
import random

RANDOM_SEED=0
N_LARGE=1000
N_SMALL=20

class Test_Chromosome():
# run nose tests in parallel (multiprocessing module)
  _multiprocess_can_split_ = True
  #_multiprocess_shared_

  def set_random_seed(self):
    """Create deterministic chromosomes by setting its random seed."""
    Chromosome.random_seed(RANDOM_SEED)
    #random returns different numbers for different versions of python

  def test_constructor_int(self):
    self.set_random_seed()
    c1 = Chromosome(10, random=False)
    np.testing.assert_array_equal(c1.path, np.asarray([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))

  def test_constructor_array(self):
    a1 = np.arange(500)
    c1 = Chromosome(a1, random=False)
    a2 = np.copy(a1)
    np.random.shuffle(a2)
    c2 = Chromosome(a2, random=False)
    np.testing.assert_array_equal(c1.path, a1)
    np.testing.assert_array_equal(c2.path, a2)

  def test_constructor_chromosome(self):
    c1 = Chromosome(500, random=False)
    c2 = Chromosome(c1, random=False)
    np.testing.assert_array_equal(c1.path, c2.path)

  def test__ne__true(self):
    c1 = Chromosome([0,1,2,3,4,5,6,7,8], random=False)
    c2 = Chromosome([0,8,7,6,5,1,2,3,4], random=False)
    c3 = Chromosome(500, random=False)
    assert c1 != c3
    assert c1 != c2
    assert c2 != c3

  def test__ne__false_basic(self):
    c1 = Chromosome([0,1,2,3,4,5], random=False)
    c2 = Chromosome([0,1,2,3,4,5], random=False)
    assert_equal(False, c1 != c2)

  def test__ne__false_large(self):
    c1 = Chromosome(500, random=False)
    c2 = Chromosome(c1, random=False)
    assert_equal(False, c1 != c2)
    assert_not_equal(id(c1), id(c2))

  def test__eq__true_basic(self):
    c1 = Chromosome([9,8,7,6,5,4,3,2,1,0], random=False)
    c2 = Chromosome([9,8,7,6,5,4,3,2,1,0], random=False)
    assert c2 == c1
    assert_not_equal( id(c2), id(c1))

  def test__eq__true_large(self):
    c1 = Chromosome(500, random=False)
    c2 = Chromosome(500, random=False)
    assert c2 == c1
    assert_not_equal( id(c2), id(c1))

  def test__eq__false_basic(self):
    c1 = Chromosome([0,1,2,3,4,5,6,7,8,9], random=False)
    c2 = Chromosome([7,8,9,3,4,5,1,2,0,6], random=False)
    assert_equal(False, c2 == c1)
    assert_not_equal( id(c2), id(c1))

  def test__eq__false_large(self):
    c1 = Chromosome(500, random=False)
    c2 = Chromosome(400, random=False)
    assert_equal(False, c2 == c1)
    assert_not_equal( id(c2), id(c1))

  def test_copy(self):
    c1 = Chromosome(500, random=True)
    c2 = c1.copy()
    np.testing.assert_array_equal(c2.path, c1.path)
    assert_not_equal( id(c2), id(c1))

  def test_order_mutate(self):
    self.set_random_seed()
    c1 = Chromosome(15, random=False)
    #c1.path.sort()
    c1.order_mutation() 
    np.testing.assert_array_equal(
      c1.path,
      np.asarray([ 0,  2,  3,  4,  5,  6,  1,  7,  8,  9, 10, 11, 12, 13, 14])
    )

  def test_roll_mutation(self):
    c1 = Chromosome(10, random=False)
    c1.roll_mutation()
    arr = np.arange(10)
    arr = np.roll(arr, 1)
    np.testing.assert_array_equal( c1.path, arr)

  def test_crossover(self):
    self.set_random_seed()
    c1 = Chromosome(10, random=True)
    c2 = Chromosome(10, random=True)
    c1copy = c1.copy()
    print(c1.path)
    print(c2.path)
    child1, child2 = c1.crossover(c2)
    assert c1copy == c1
    np.testing.assert_array_equal(child1.path, [2, 1, 8, 9, 0, 6, 7, 3, 4, 5])
    np.testing.assert_array_equal(child2.path, [3, 5, 8, 2, 9, 4, 1, 6, 7, 0])

  def test_mutation_path_size(self):
    for _ in range(N_LARGE):
      n = random.randint(2, 350)
      c = Chromosome(n, random=True)
      for _ in range(N_SMALL):
        assert_equal(c.path.size, c.mutate().path.size)

  def test_creation_path_uniqueness(self):
    for _ in range(N_LARGE):
      n = random.randint(2,350)
      c = Chromosome(n, random=True)
      u = np.unique(c.path)
      assert_equal(u.size, c.path.size)

  def test_mutation_path_uniqueness(self):
    for _ in range(N_LARGE):
      n = random.randint(2, 350)
      c = Chromosome(n, random=True)
      for _ in range(N_SMALL):
        assert_equal( c.path.size, np.unique(c.mutate().path).size )
