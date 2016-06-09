  def path_cost(self, l):
    cost = 0
    previous_n = self.source
    for n in l:
      try:
        cost += self.g[previous_n][n]['weight']
      except KeyError:
        print("cost={c} previous_n={p} n={n}".format(c=cost, p=previous_n, n=n))
        print("nodes {l}".format(l=list(self.g.nodes())))
        print("{p}->{n} in edges:{bool}".format(p=previous_n, n=n,
          bool=(previous_n, n) in list(self.g.edges())))
        print("key {k} in dict g:{bool}".format(k=previous_n, bool=previous_n in self.g))
        print("try g[{k}]: {t}".format(k=previous_n, t=self.g[previous_n]))
        print("key {k} in dict g[{p}]:{bool}".format(k=n, p=previous_n,
          bool=n in self.g[previous_n]))
        #print("try g[{k1}][{k2}]:{t}".format(k1=previous_n, k2=n, t=self.g[previous_n][n]))
        raise
      previous_n = n
    cost += self.g[previous_n][self.source]['weight']
    return cost
