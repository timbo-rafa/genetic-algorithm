#!/usr/bin/env python

import numpy as np

class Chromosome():
  """ A chromosome representing a possible solution for a TSP problem.
  The array represents the order in which the cities should be visited"""

  def __init__(self, arg, random=True):
    if (isinstance(arg, int)):
      self.path = np.arange(arg)
      if (random):
        np.random.shuffle(self.path)
    elif (isinstance(arg, Chromosome)):
      self.path = np.copy(arg.path)
    elif (isinstance(arg, (np.ndarray, list))):
      self.path = np.copy(arg)
    else:
      print(type(arg))
      raise TypeError("Invalid argument for chromosome constructor.")

  def __eq__(self, chr2):
    return np.array_equal(self.path, chr2.path)
    #return self.path == chr2.path

  def __ne__(self, chr2):
    return not self.__eq__(chr2)

  def __getitem__(self, index):
    return self.path[index]

  @classmethod
  def random_seed(self, seed):
    np.random.seed(seed)

  def crossover(self, chr2):
    """Generate two new chromosomes exchanging the order of a random subset of cities
    between this chromosome and another (chr2)."""
    return self.__ordered_crossover_single(chr2)

  def __ordered_crossover_single_list(self, chr2):
    new_chr = self.copy()
    new_chr2 = chr2.copy()
    c2 = list(chr2.path)

    gene_mask = np.random.rand(len(self.path)) > 0.5
    sel1 = []
    sel2 = []
    pos1 = []
    pos2 = []
    for idx, b in enumerate(gene_mask):
      if b:
        sel1.append(self[idx])
      else:
        sel2.append(self[idx])
        pos1.append(idx)
        pos2.append(c2.index(self[idx]))
    pos2.sort()
    for pi1, p2 in enumerate(pos2):
      sel1.insert(pos1[pi1], chr2[p2])
      #new_chr2.path.pop(p2)
      np.delete(new_chr2.path, p2)
      np.insert(new_chr2.path, p2, sel2.pop(0))
      #new_chr2.path.insert(p2,sel2.pop(0))
    new_chr.path = np.asarray(sel1)

    return new_chr, new_chr2

  def __ordered_crossover_single(self, chr2):
    new_chr = self.copy()
    new_chr2 = chr2.copy()

# pick random elements of element 1
    gene_mask = np.random.rand(len(self.path)) > 0.5
    #print(gene_mask)
    gene_idx = np.where(gene_mask)
# get the fixed elements
    fix1 = self[gene_idx]
    not_gene_idx = np.where(np.logical_not(gene_mask))
# get the elements that are gonna swap order
    swap1 = self[not_gene_idx]
# select the fixed elements in chr2(boolean)
    gene2_mask = np.in1d(chr2.path, fix1, assume_unique=True)
# get the elements that are gonna swap order
    not_gene2_idx = np.where(np.logical_not(gene2_mask))
    swap2 = chr2.path[not_gene2_idx]
# swap first chromosome's selected elements by second chromosome elements
# (reordering by 2nd chromosome)
    new_chr.path[not_gene_idx] = swap2
# swap second chromosome's selected elements by first chromosome elements
# (reordering according to 1st chromosome's order)
    new_chr2.path[not_gene2_idx] = swap1

    #print("gene_mask={m}".format(m=gene_mask))
    #print("fix1={f}".format(f=fix1))
    #print("swap1={s}".format(s=swap1))
    #print("swap2={s}".format(s=swap2))
    return new_chr,new_chr2

  def order_mutation(self):
    """Returns this chromosome with gene1 removed from its position and inserted before gene2."""
    i = np.random.choice(np.arange(self.path.size), size=2, replace=False)
    i1 = i[0]
    i2 = i[1]
    gene1 = self.path[i1]
    #print(gene1, gene2)
    self.path = np.delete(self.path, i1)
    self.path = np.insert(self.path, i2, gene1)
    return self

  def roll_mutation(self):
    """Returns this chromosome with the last city as the first visited
    and the others cities shifted appropriately"""
    #shift_width = np.random.choice(np.arange(1,self.path.size),1)
    shift_width = 1
    self.path = np.roll(self.path, shift_width)
    return self
    
  def mutate(self):
    """Interface for mutate function.
    Change the chromosome path using the biological concept of mutation"""
    return self.order_mutation()

  def copy(self):
    new_chr = Chromosome(self)
    return new_chr

# paper on mutation
# http://www.ceng.metu.edu.tr/~ucoluk/research/publications/tspnew.pdf
# order mutation
# http://www.permutationcity.co.uk/projects/mutants/tsp.html
