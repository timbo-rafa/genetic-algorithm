"""
Module responsible for graph handling
"""

import networkx as nx
import random

MAX_GRAPH_WEIGHT=200
FILENAME="graph.gpickle"

class Graph():
  def w(self, i, j):
    return j * 100 + 1

  def weight_generator(self):
    for i in range(0, self.n):
      for j in range(0, self.n):
        if (i != j):
          #self.g.add_edge(i,j,weight=random.randint(0,MAX_GRAPH_WEIGHT))
          if ( i > j):
            self.g.add_edge(i,j,weight=self.w(i,j))
          else:
            self.g.add_edge(i,j,weight=self.w(j,i))

  def generate(self):
    self.g = nx.Graph()
    self.weight_generator()
    self.filename="graph{nodes}_{edges}.gpickle".format(
      nodes=self.g.number_of_nodes(), edges=self.g.size())
    return self.g

  def __copy(self, g):
    self.g = g

  def read(self):
    return nx.read_gpickle(self.filename)

  def __init__(self, n, source=None, save=True, option='generate', filename=FILENAME):
    self.create =  {
      'generate' : self.generate,
      'read': self.read,
    }
    if (source == None):
      self.source = n - 1
    else:
      self.source = source
    self.n = n
    self.save = save
    self.filename = filename
    self.g = self.create[option]()
    if self.save:
      self.write()
    
  def write(self):
    nx.write_gpickle(self.g, self.filename)

  def path_cost(self, l):
    cost = 0
    previous_n = self.source
    for n in l:
      cost += self.g[previous_n][n]['weight']
      previous_n = n
    cost += self.g[previous_n][self.source]['weight']
    return cost

if __name__ == '__main__':
  Graph(option='generate')
  Graph(option='read')
