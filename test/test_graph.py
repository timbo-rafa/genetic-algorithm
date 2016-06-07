from ga import Chromosome
from graph import Graph
from nose.tools import assert_equal, assert_not_equal
import numpy as np

class Test_Graph():
  def __init__(self):
    self.g3 = Graph(n=3,source=2,save=False, option='generate')
    self.g4 = Graph(n=4,source=3,save=False, option='generate')
    self.g5 = Graph(n=5,source=4,save=False, option='generate')
    self.g6 = Graph(n=6,source=5,save=False, option='generate')

  def test_path_cost(self):
    g = Graph(n=6, source=5, save=False, option='generate')
    w = [1, 20, 400, 5000, 10000, 4]
    g.g[5][0]['weight'] = w[0]
    g.g[0][1]['weight'] = w[1]
    g.g[1][2]['weight'] = w[2]
    g.g[2][3]['weight'] = w[3]
    g.g[3][4]['weight'] = w[4]
    g.g[4][5]['weight'] = w[5]
    path = np.array([0,1,2,3,4])
    cost = sum(w)
    assert_equal(cost, g.path_cost(path))

#  def test_path_cost_30(self):
#    assert_equal(self.g3.path_cost([0,1]),200+100+201)
#
#  def test_path_cost_40(self):
#    assert_equal(self.g4.path_cost([0,1,2]),300+100+201+302)
#
#  def test_path_cost_50(self):
#    assert_equal(self.g5.path_cost([0,1,2,3]),400+100+201+302+403)
#
#  def test_path_cost_100(self):
#    assert_equal(self.g5.path_cost([3,1,2,0]),403+301+201+200+400)
