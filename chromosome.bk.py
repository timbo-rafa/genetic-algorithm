#!/usr/bin/env python

import random
import numpy as np

class Chromosome():
  """ A chromosome representing a possible solution for a TSP problem.
  The array represents the order in which the cities should be visited"""

  def __init__(self, arg, random=False):
    if (isinstance(arg, int)):
      self.path = np.arange(arg)
      if (random):
        np.random.shuffle(self.path)
    elif (isinstance(arg, (np.ndarray, list))):
      self.path = np.copy(arg)
    else:
      raise TypeError("Invalid argument for chromosome constructor.")

  def __eq__(self, chr2):
    return np.array_equal(self.path, chr2.path)
    #return self.path == chr2.path

  def __getitem__(self, index):
    return self.path[index]

  @classmethod
  def random_seed(self, seed):
    np.random.seed(seed)

  def crossover(self, chr2):
    return self.ordered_crossover_single(chr2)

  def ordered_crossover_single(self, chr2):
    new_chr = self.copy()
    new_chr2 = chr2.copy()

# pick random elements of element 1
    gene_mask = np.random.rand(len(self.path)) > 0.5
    print(gene_mask)
# get the random elements' indexes
    gene_idx = np.where(gene_mask)
# get their complementary indexes
    not_gene_idx = np.where(np.logical_not(gene_mask))
# get the selected elements
    fix1 = self[gene_idx]
# get the complementary elements
    not_sel1 = self[not_gene_idx]
# select the complementary elements in chr2(boolean)
    gene2_mask = np.in1d(chr2.path, sel1, assume_unique=True)
# get their indexes of chr2
    gene2_idx = np.where(gene2_mask)
# get the elements(now ordered according to second chromosome)
    sel2 = chr2.path[gene2_idx]

# swap first chromosome's selected elements by second chromosome elements
# (reordering by 2nd chromosome)
    new_chr.path[not_gene_idx] = sel2

# swap second chromosome's selected elements by first chromosome elements
# (reordering according to 1st chromosome's order)
    not_gene2_idx = np.where(np.logical_not(gene2_mask))
    new_chr2.path[not_gene2_idx] = not_sel1

    return new_chr,new_chr2

  def order_mutation(self):
    """Returns this chromosome with gene1 removed from its position and inserted before gene2 """
    genes = random.sample(self.path,2)
    gene1 = genes[0]
    gene2 = genes[1]
    print(gene1, gene2)
    self.path.remove(gene1)
    self.path.insert(self.path.index(gene2), gene1)
    return self
    
  def mutate(self, gene1=None, gene2=None):
    return self.order_mutation

  def copy(self):
    new_chr = Chromosome(self.path.size)
    new_chr.path = np.copy(self.path)
    return new_chr

# paper on mutation
# http://www.ceng.metu.edu.tr/~ucoluk/research/publications/tspnew.pdf
# order mutation
# http://www.permutationcity.co.uk/projects/mutants/tsp.html
